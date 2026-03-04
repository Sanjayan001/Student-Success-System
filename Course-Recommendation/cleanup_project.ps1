# Project Cleanup Script
# Removes temporary, test, and unused files

Write-Host "Starting project cleanup..." -ForegroundColor Cyan

# Files to delete
$patterns = @(
    "recommendations_S*.csv",      # 150+ test recommendation files
    "explain_*.py",                 # Old explanation test scripts
    "test_*.py",                    # Test scripts (except if needed)
    "compare_mmr_diversity.py",     # MMR comparison test
    "meta_learner.py",              # Rejected meta-learner
    "meta_learner_weights.pkl",     # Rejected weights
    "train.txt",                    # Temporary text file
    "create_student_level_labels.py", # Old preprocessing
    "create_better_features.py",    # Old feature engineering
    "show_model_accuracy.py",       # Replaced by visualize
    "evaluate_recommendations.py"   # Old evaluation script
)

$deletedCount = 0
$totalSize = 0

foreach ($pattern in $patterns) {
    $files = Get-ChildItem -Path $PSScriptRoot -Filter $pattern -File -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        $size = $file.Length
        $totalSize += $size
        Write-Host "  Deleting: $($file.Name) ($([math]::Round($size/1KB, 2)) KB)" -ForegroundColor Yellow
        Remove-Item $file.FullName -Force
        $deletedCount++
    }
}

Write-Host "`nCleanup Summary:" -ForegroundColor Green
Write-Host "  Files deleted: $deletedCount" -ForegroundColor White
Write-Host "  Space freed: $([math]::Round($totalSize/1MB, 2)) MB" -ForegroundColor White
Write-Host "`nProject cleaned successfully! ✓" -ForegroundColor Green
