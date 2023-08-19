#Run as: powershell -ExecutionPolicy RemoteSigned .\thisFile.ps1
#define constants
$OutputEncoding=[Console]::OutputEncoding
$OutputEncoding=[System.Text.Encoding]::GetEncoding('Shift_JIS')
$bgColor = "wheat"
$fgColor = "#2e4054"
$smallFont = "Microsoft Sans Serif,10"
$dateTime = Get-Date -DisplayHint DateTime
# init powershell gui
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

[System.Windows.Forms.Application]::EnableVisualStyles()
# create new form
$displayWidgetsForm = New-Object system.Windows.Forms.Form
#define window size
$displayWidgetsForm.ClientSize = '240,380'
$displayWidgetsForm.text = 'fetch MLIT - ext TXT - XLS & Mail'
$displayWidgetsForm.BackColor = $bgColor

# main title of window
$titel = New-Object system.Windows.Forms.Label
$titel.text = "Fetch recall info from MLIT.go.jp"
$titel.AutoSize = $true
$titel.width = 25
$titel.height = 10
$titel.location = New-Object System.Drawing.Point(15,10)
$titel.Font = 'Microsoft Sans Serif, 11'
$titel.ForeColor = $fgColor
# display output on label,
$userOutLabel = New-Object system.Windows.Forms.TextBox
$userOutLabel.multiline = $true #notAvail on Label
$userOutLabel.text = ""
$userOutLabel.AutoSize = $false
$userOutLabel.width = 210
$userOutLabel.height = 125
$userOutLabel.Visible = $false
$userOutLabel.Font = $smallFont
# $userOutLabel.enabled = $false
$userOutLabel.location = New-Object System.Drawing.Point(15,210)

#calendar widget
$calendar = New-Object Windows.Forms.MonthCalendar -Property @{
   ShowTodayCircle   = $false
   MaxSelectionCount = 1
}
$calendar.MaxDate = $dateTime
$calendar.location = New-Object System.Drawing.Point(20,40)
$displayWidgetsForm.Controls.Add($calendar)
#adding buttons
$clickBtn = New-Object system.Windows.Forms.Button
$clickBtn.BackColor = $fgColor
$clickBtn.text = "Get"
$clickBtn.width = 90
$clickBtn.height = 30
$clickBtn.location = New-Object System.Drawing.Point(130,340)
$clickBtn.Font = $smallFont
$clickBtn.ForeColor = "#ffffff"

$cancelBtn = New-Object system.Windows.Forms.Button
$cancelBtn.BackColor = "#ffffff"
$cancelBtn.text = "Open Excel"
$cancelBtn.Size = New-Object System.Drawing.Size(90,30)
# $cancelBtn.width = 90 # $cancelBtn.height = 30
$cancelBtn.location = New-Object System.Drawing.Point(20,340)
$cancelBtn.Font = $smallFont
$cancelBtn.ForeColor = "#000"
#$cancelBtn.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
#$displayWidgetsForm.CancelButton = $cancelBtn
#$displayWidgetsForm.Controls.Add($cancelBtn)

#adding widgets to form $userInputLabel,$userInput,
$displayWidgetsForm.controls.AddRange(@($titel,$userOutLabel,$clickBtn,$cancelBtn))
$pythonExe = "d:\Python\Python-3.9.7\python.exe"
$pythonProc = @{
   FilePath = "d:\Python\Python-3.9.7\python.exe"
   RedirectStandardInput = ".\fetch_url.py"
   UseNewEnvironment = $false
}
$fetch_log = ".\fetch_url.log"
$ext_log = ".\ext_pdf.log" #might not be needed

function thisFunction {
   # Write-Host 'User input:'$userInput.Text
   $userOutLabel.Visible = $true
   # $userOutLabel.text = $userInput.Text
   $date = $calendar.SelectionStart
   Write-Host "Consult time: $dateTime"
   $doneText = "Request date $($date.ToShortDateString()) `r`n"
   $userOutLabel.text = $doneText
   Start-Process -FilePath $pythonExe -ArgumentList ".\fetch_url.py",$date.ToShortDateString() -RedirectStandardOutput $fetch_log -Wait -NoNewWindow
   # Start-Sleep -Seconds 5 # wait for python to finish
   $grepEve = Select-String -Path $fetch_log -Pattern "downloading"
   $numEve = $grepEve -Split " "
   # Write-Host "numFiles:$grepEve and $($numEve[1])"
   # Write-Host $(Select-String -Path $fetch_log -Pattern "downloading")
   if($($numEve[1]) -eq "0"){
       $doneText = $doneText + "No such date on pressRelease`r`nTry another date"
   }else{
       Write-Host "Found $($numEve[1]) event(s)"
       $doneText = $doneText + "Downloading $($numEve[1]) PDF file(s)...   `r`n"
       $userOutLabel.text = $doneText
       $pdfs = Get-Content -Path $fetch_log -Tail $numEve[1]
       
       $eve = $pdfs -Split " "
       $jdx = 0
       for($idx=0;$idx -le ($numEve[1]-1);$idx++){
           $doneText = $doneText + "File $($idx+1) : extracting info... `r`n"
           $userOutLabel.text = $doneText
           $jdx += 2
           $thisFile = $eve[$($jdx+$idx)]
           Write-Host "Got this file:"$thisFile
           Start-Process -FilePath $pythonExe -ArgumentList ".\miner_test.py","$thisFile" -RedirectStandardOutput $ext_log -Wait -NoNewWindow
           #Wait-Process -InputObject ?
           #No longer avail $outData = Get-Content -Path $ext_log
           $doneText = $doneText + "      writing to Excel file...`r`n"
           $userOutLabel.text = $doneText
           Start-Process -FilePath $pythonExe -ArgumentList ".\xls_win32.py" -RedirectStandardOutput $ext_log -Wait -NoNewWindow
           # Start-Sleep -Seconds 4
       }
       $doneText = $doneText + "Done"
       #$userOutLabel.text = $doneText
       # "Opening Outlook..."
       # $doneText = $doneText -join "`r`n" for arrays 
   }

   $userOutLabel.text = $doneText
   # Write-Host "date selected: $($date.ToShortDateString())"
   # Write-Host $doneText
}
function openExcel {
   Write-Host $PSScriptRoot

   $xlsFile = $PSScriptRoot + "\recall_info_02.xlsm"
   $Excel = New-Object -ComObject Excel.Application
   $Excel.Visible = $true
   $workBook = $Excel.WorkBooks.Open($xlsFile)
}

$clickBtn.Add_Click({ thisFunction })

$cancelBtn.Add_Click({ openExcel })
#display form
$result = $displayWidgetsForm.ShowDialog()

if ($result -eq [Windows.Forms.DialogResult]::OK) {
   $date = $calendar.SelectionStart
   Write-Host "date selected: $($date.ToShortDateString())"
}
