$services = Get-WmiObject Win32_Service | Select-Object Caption, CheckPoint, Description, DisplayName, InstallDate, PathName, Name, ProcessId, Started, StartMode, StartName, State
$kbs = Get-WMIObject WIn32_QuickFixEngineering | Select-Object Caption, Description, FixComments, HotFixID, InstallDate, Name, Status, InstalledBy
$shares = Get-WmiObject Win32_Share | Select-Object Caption, Description, InstallDate, MaximumAllowed, Name, Path, Status, Type
$dirs = Get-WmiObject Win32_Directory | Where-Object {$_.System -eq $False} | Select-Object Archive, Caption, CreationDate, Extension, FileType, FileSize, Hidden, LastAccessed, LastModified, InstallDate

@"
{
  "services": [$($services_formatted = New-Object System.Collections.Generic.List[System.Object];foreach($service in $services){
    $services_formatted.Add("
    {
      `"service_caption`": `"$($service.caption)`",
      `"service_check_point`": `"$($service.CheckPoint)`",
      `"service_description`": `"$($service.description)`",
      `"service_display_name`": `"$($service.DisplayName)`",
      `"service_install_date`": `"$($service.InstallDate)`",
      `"service_path_name`": `"$(if($null -ne $service.PathName){($service.PathName).replace('\', '\\').replace('"', '')}else{"null"})`",
      `"service_name`": `"$($service.name)`",
      `"service_process_id`": `"$($service.ProcessId)`",
      `"service_started`": `"$($service.Started)`"
    }
    ")
  }($services_formatted -join ','))],
  "kbs": [$($kbs_formatted = New-Object System.Collections.Generic.List[System.Object];foreach($kb in $kbs){
    $kbs_formatted.Add("
    {
      `"kb_caption`": `"$($kb.caption)`",
      `"kb_description`": `"$($kb.Description)`",
      `"kb_comments`": `"$($kb.FixComments)`",
      `"kb_id`": `"$($kb.HotFixID)`",
      `"kb_install_date`": `"$($kb.InstallDate)`",
      `"kb_name`": `"$($kb.name)`",
      `"kb_status`": `"$($kb.status)`",
      `"kb_installed_by`": `"$($kb.InstalledBy)`"
    }
    ")
  } ($kbs_formatted -join ',') )],
  "shares": [$($shares_formatted = New-Object System.Collections.Generic.List[System.Object];foreach($share in $shares){
    $shares_formatted.Add("
    {
      `"share_caption`": `"$($share.caption)`",
      `"share_description`": `"$($share.description)`",
      `"share_install_date`": `"$($share.InstallDate)`",
      `"share_maximum_allowed`": `"$($share.MaximumAllowed)`",
      `"share_name`": `"$($share.name)`",
      `"share_path`": `"$($share.Path)`",
      `"share_status`": `"$($share.status)`",
      `"share_type`": `"$($share.type)`"
    }
    ")
  }($shares_formatted -join ','))],
  "dirs: [$($dirs_formatted = New-Object System.Collections.Generic.List[System.Object];foreach($dir in $dirs){
    $dirs_formatted.Add("
    {
      `"dir_is_archive`": $(($dir.Archive | Out-String).toLower()),
      `"dir_caption`": `"$(($dir.caption).replace('\', '\\'))`",
      `"dir_creation_date`": `"$($dir.CreationDate)`",
      `"dir_extension`": `"$($dir.extension)`",
      `"dir_file_type`": `"$($dir.FileType)`",
      `"dir_file_size`": `"$($dir.FileSize)`",
      `"dir_is_hidden`": $(($dir.Hidden | Out-String).toLower()),
      `"dir_last_accessed`": `"$($dir.LastAccessed)`",
      `"dir_last_modified`": `"$($dir.LastModified)`",
      `"dir_install_date`": `"$($dir.InstallDate)`"
    }
    ")
  } ($dirs_formatted -join ','))]
}
"@