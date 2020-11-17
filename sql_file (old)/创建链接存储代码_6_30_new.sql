CREATE OR REPLACE FUNCTION Create_Link( folderName varchar,address_ varchar,
	name_ varchar, userName varchar) RETURNS integer AS $$
declare
    answer integer;
    rec RECORD;
    fit boolean;
    folderid_ integer;
    userid_ integer;
 
BEGIN
    answer=0;
    fit=false;
    -- FOR rec IN SELECT * FROM user_ 
    -- LOOP
    --     IF rec.user_name=userName
    --     THEN
    --         userid_=rec.user_id;
    --     END IF;
    -- END LOOP;
    SELECT u.user_id INTO userid_ FROM user_ as u WHERE u.user_name = userName;

    FOR rec IN SELECT * FROM folder_ 
    LOOP
        IF rec.folder_name=folderName
        THEN
            folderid_=rec.folder_id;
            fit = true;
        END IF;
    END LOOP;

    IF fit = FALSE
    THEN
        INSERT INTO public.folder_(folder_name, user_id) VALUES (folderName,userid_);
        SELECT f.folder_id INTO folderid_ FROM folder_ as f WHERE f.folder_name=folderName;
    END IF;

    INSERT INTO public.link_ VALUES(default,address_,name_,userid_,folderid_);
    
    return answer;
END
$$language plpgsql;