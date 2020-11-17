SELECT link_address
    FROM uName_fName_url
    WHERE link_id in (
        select MAX(link_id) 
            FROM uName_fName_url 
            WHERE folder_name='@@keyword@@' AND user_name='@@userName@@'
        );