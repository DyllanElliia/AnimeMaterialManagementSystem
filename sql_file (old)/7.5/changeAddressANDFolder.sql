CREATE OR REPLACE FUNCTION Change_Address_FolderName(   linkAddress_ varchar, userName_ varchar,
											            newLinkAddress_ varchar,
									                    newFolderName_ varchar
	 ) RETURNS boolean AS $$
declare
    linkid_ integer;
    userid_ integer;
	newFolderID integer;
BEGIN
    SELECT user_id INTO userid_ FROM public.user_ WHERE user_name= userName_;
    SELECT folder_id INTO newFolderID FROM public.folder_ WHERE folder_name = newFolderName_;
    if newFolderID IS NULL
    THEN
        INSERT INTO public.folder_(
            folder_id, folder_name, user_id)
            VALUES (DEFAULT, newFolderName_, userid_);
        SELECT folder_id INTO newFolderID FROM public.folder_ WHERE folder_name = newFolderName_;
    END IF;
    if newFolderID IS NULL OR userid_ IS NULL
    THEN
        return FALSE;
    END IF;
    UPDATE public.link_ SET link_address = newLinkAddress_, folder_id = newFolderID
        WHERE link_address=linkAddress_;
    return TRUE;
END
$$language plpgsql;


