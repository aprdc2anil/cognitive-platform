# ===============================
# WSL Weekly Backup Script
# ===============================

$DistroName = "Ubuntu"
$BackupDir = "C:\GDrive\dev\wsl-backups\ubuntu"
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$BackupFile = "$BackupDir\ubuntu-$Timestamp.tar"

Write-Output "====================================="
Write-Output "WSL Backup Started: $(Get-Date)"
Write-Output "Distro: $DistroName"
Write-Output "Backup Dir: $BackupDir"
Write-Output "====================================="

# Ensure backup directory exists
if (!(Test-Path $BackupDir)) {
    Write-Output "Creating backup directory..."
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
}

# Shutdown WSL for filesystem consistency
Write-Output "Shutting down WSL..."
wsl --shutdown

Start-Sleep -Seconds 5

# Export WSL distribution
Write-Output "Exporting WSL snapshot..."
wsl --export $DistroName $BackupFile

if (Test-Path $BackupFile) {
    Write-Output "Backup successful: $BackupFile"
} else {
    Write-Output "Backup failed."
    exit 1
}

# Cleanup old backups (keep last 2)
Write-Output "Cleaning old backups..."

$Backups = Get-ChildItem $BackupDir -Filter "*.tar" | Sort-Object LastWriteTime -Descending

if ($Backups.Count -gt 2) {

    $BackupsToDelete = $Backups | Select-Object -Skip 2

    foreach ($Backup in $BackupsToDelete) {
        Write-Output "Deleting old backup: $($Backup.Name)"
        Remove-Item $Backup.FullName
    }

} else {
    Write-Output "No old backups to delete."
}

Write-Output "====================================="
Write-Output "WSL Backup Completed: $(Get-Date)"
Write-Output "====================================="