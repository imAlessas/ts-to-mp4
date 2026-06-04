#!/usr/bin/env python3
"""
Convert all .ts files in the 'source' folder (parent of script folder) to MP4 format inside a 'converted' subfolder (also in parent folder).
Uses ffmpeg (requires ffmpeg.exe in the same folder as script or in system PATH).
"""

import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, MofNCompleteColumn
from rich.style import Style
from rich.panel import Panel

# Create console with colorful output
console = Console()

def convert_ts_to_mp4():
    # Get the script's directory
    script_dir = Path(__file__).parent
    
    # Parent folder (folder "a")
    parent_dir = script_dir.parent
    
    # Source folder is in the parent folder
    source_folder = parent_dir / "source"
    
    # Converted folder is also in the parent folder (not in script folder)
    converted_folder = parent_dir / "converted"
    converted_folder.mkdir(exist_ok=True)
    
    # Check if source folder exists
    if not source_folder.exists():
        console.print(f"[bold red]✗ Error:[/bold red] 'source' folder not found at [cyan]{source_folder}[/cyan]")
        return
    
    # Find all .ts files in the source folder (not in subfolders)
    # Case-insensitive for .TS and .ts
    ts_files = [f for f in source_folder.iterdir() 
                if f.is_file() and f.suffix.lower() == '.ts']
    
    if not ts_files:
        console.print("[bold yellow]⚠ No .ts files found in the 'source' folder.[/bold yellow]")
        return
    
    console.print(Panel.fit(
        f"[bold green]🎬 TS to MP4 Converter[/bold green]\n"
        f"Found [bold cyan]{len(ts_files)}[/bold cyan] file(s) to convert",
        border_style="green"
    ))
    
    # Check if ffmpeg is available
    ffmpeg_path = script_dir / "ffmpeg.exe"
    if ffmpeg_path.exists():
        ffmpeg_cmd = str(ffmpeg_path)
        console.print("[green]✓[/green] Using ffmpeg.exe from script folder.")
    else:
        ffmpeg_cmd = "ffmpeg"
        console.print("[green]✓[/green] Using ffmpeg from system PATH.")
    
    # Convert each .ts file to MP4 with progress bar
    converted_count = 0
    error_count = 0
    
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Converting...", total=len(ts_files))
        
        for ts_file in ts_files:
            mp4_filename = ts_file.stem + ".mp4"
            mp4_path = converted_folder / mp4_filename
            
            console.print(f"\n[bold yellow]→ Converting:[/bold yellow] [cyan]{ts_file.name}[/cyan] → [green]{mp4_filename}[/green]")
            
            # ffmpeg command to convert TS to MP4 (copy codec = fast, no re-encoding)
            cmd = [
                ffmpeg_cmd,
                "-i", str(ts_file),
                "-c:v", "copy",
                "-c:a", "copy",
                "-movflags", "+faststart",
                "-y",  # Overwrite output file if it exists
                str(mp4_path)
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    console.print(f"[bold green]✓ Successfully converted:[/bold green] [cyan]{ts_file.name}[/cyan]")
                    converted_count += 1
                else:
                    console.print(f"[bold red]✗ Error converting {ts_file.name}:[/bold red]")
                    console.print(f"[red]{result.stderr[:200] if result.stderr else 'Unknown error'}[/red]")
                    error_count += 1
            except FileNotFoundError:
                console.print("[bold red]✗ Error:[/bold red] ffmpeg is not installed.")
                console.print("[yellow]Download ffmpeg.exe and place it in this folder, or add to PATH.[/yellow]")
                console.print(f"[cyan]Download: https://ffmpeg.org/download.html[/cyan]")
                return
            except Exception as e:
                console.print(f"[bold red]✗ Unexpected error:[/bold red] [red]{e}[/red]")
                error_count += 1
            
            progress.update(task, advance=1)
    
    # Final summary
    console.print("\n" + "="*60)
    if error_count == 0:
        console.print(Panel.fit(
            f"[bold green]🎉 Conversion Complete![/bold green]\n\n"
            f"Successfully converted: [bold cyan]{converted_count}[/bold cyan] file(s)\n"
            f"MP4 files are in the '[bold green]converted[/bold green]' folder",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            f"[bold yellow]⚠ Conversion Finished with Errors[/bold yellow]\n\n"
            f"Successfully converted: [bold green]{converted_count}[/bold green] file(s)\n"
            f"Failed: [bold red]{error_count}[/bold red] file(s)\n"
            f"MP4 files are in the '[bold green]converted[/bold green]' folder",
            border_style="yellow"
        ))
    console.print("="*60)


if __name__ == "__main__":
    convert_ts_to_mp4()
