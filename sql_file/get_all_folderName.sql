SELECT folder_name FROM folder_ WHERE user_id in (
    SELECT user_id FROM user_ WHERE user_name = '@@userName@@'
);