CREATE OR REPLACE FUNCTION Create_Link( folderName_ varchar,pictureAddress_ varchar,
	pictureName_ varchar, userName_ varchar) RETURNS boolean AS $$
declare
 
    folderid_ integer;
    userid_ integer;
 
BEGIN
   
   
    SELECT user_id INTO userid_ FROM user_ WHERE user_name = userName_;
	SELECT folder_id INTO folderid_ FROM folder_ WHERE folder_name=folderName_
	and user_id = userid_;
	
    
    IF folderid_ is NULL
    THEN
        INSERT INTO folder_ VALUES (default,folderName_,userid_);
        SELECT folder_id INTO folderid_ FROM folder_ WHERE folder_name=folderName_;
    END IF;

    INSERT INTO picture_ VALUES(default,pictureName_,pictureAddress_,folderid_);
    
    return true;
END
$$language plpgsql;