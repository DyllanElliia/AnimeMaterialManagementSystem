SELECT l.link_id, l.link_address FROM link_ as l
    WHERE
    l.link_id in
    (
        SELECT link_id FROM uName_fName_url
            WHERE   folder_name = '@@folderName@@' AND
                    user_name = '@@userName@@'
    )
    AND l.link_name='@@linkName@@';