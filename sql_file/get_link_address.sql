SELECT pi.picture_id, pi.picture_address FROM picture_ as pi
    WHERE
    pi.picture_id in
    (
        SELECT picture_id FROM all_show
            WHERE   folder_name = '@@folderName@@' AND
                    user_name = '@@userName@@'
    )
    AND pi.picture_name='@@linkName@@';