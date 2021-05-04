CREATE OR REPLACE FUNCTION Change_Address_FolderName
( pictureAddress_ varchar,
													userName_ varchar,
													 newPictureAddress_ varchar,
													new_folder_name_ varchar)
RETURNS boolean AS $$

declare
    Pictureid_ integer;
    userid_ integer;
	newFolderID integer;
BEGIN
    select user_id
    into userid_
    from user_
    where user_name=userName_;

    select picture_id
    into Pictureid_
    from all_show
    where user_id=userid_ and picture_address=pictureAddress_;

    select folder_id
    into newFolderID
    from all_show
    where folder_name=new_folder_name_ and user_id=userid_
    ;

    if newFolderID is NULL
	then
    insert into folder_
    values
        (default, new_folder_name_, userid_);
end
if;

	select folder_id
into newFolderID
from folder_
where folder_name=new_folder_name_ and user_id=userid_;

if newFolderID IS NULL OR userid_ IS NULL OR Pictureid_ is NULL
    THEN
return FALSE;
END
IF;

	UPDATE picture_ SET picture_address = newPictureAddress_, folder_id = newFolderID
        WHERE picture_id=Pictureid_;

return TRUE;
END
$$language plpgsql;
	