SELECT folder_name FROM folder_
    WHERE folder_id in (SELECT max(folder_id)FROM all_show WHERE user_name = '@@userName@@')