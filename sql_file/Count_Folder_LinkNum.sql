SELECT picture_address
    FROM all_show
    WHERE picture_id in (
        select MAX(picture_id) 
            FROM all_show
            WHERE folder_name='@@keyword@@' AND user_name='@@userName@@'
        );