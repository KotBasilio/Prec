# Fetch current user language list
$LangList = Get-WinUserLanguageList

# Display the original list
Write-Host "Original language list:" -ForegroundColor Cyan
$LangList | Format-Table LanguageTag, @{n='InputMethodTips';e={$_.InputMethodTips}} -AutoSize
Write-Host ''


Write-Host "`nInspecting InputMethodTips property types and values:" -ForegroundColor Yellow

$removedCount = 0

# Iterate over a snapshot so we can remove safely
foreach ($lang in $LangList.ToArray()) {
    $tips = $lang.InputMethodTips -join ','
    Write-Host "LanguageTag: $($lang.LanguageTag)  InputMethodTips: $tips" -ForegroundColor Cyan

    $answer = Read-Host "Remove this layout? (Y/N)"
    if ($answer -match '^[Yy]') {
        $LangList.Remove($lang)
        Write-Host "  → Removed $($lang.LanguageTag)" -ForegroundColor Green
    }
    else {
        Write-Host "  → Kept    $($lang.LanguageTag)" -ForegroundColor Yellow
    }
    Write-Host ''
}



# Report what happened
if ($removedCount -gt 0) {
    Write-Host "Removed $removedCount English (en-GB) layout entry." -ForegroundColor Green
} else {
    Write-Host "No English (en-GB) layouts found to remove." -ForegroundColor Yellow
}
Write-Host ''

# Apply the cleaned-up list back to the user profile
Set-WinUserLanguageList $LangList -Force

# Fetch and display the updated list
Write-Host "Updated language list:" -ForegroundColor Cyan
Get-WinUserLanguageList | Format-Table LanguageTag, @{n='InputMethodTips';e={$_.InputMethodTips}} -AutoSize
