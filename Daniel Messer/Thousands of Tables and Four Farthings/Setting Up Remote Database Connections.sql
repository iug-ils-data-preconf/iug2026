/* SETTING UP REMOTE CONNECTIVITY TO OTHER SQL SERVERS */

/* ----- Create a link to the remote server ----- */
EXEC sp_addlinkedserver 
    @server = 'LibraryName',  -- Name you'll use to reference it
    @srvproduct = '', -- Should be empty or NULL
    @provider = 'MSOLEDBSQL', -- UseMSOLEDBSQL
    @datasrc = '172.55.55.255,1433'  -- When using TCP/IP, provide the port number

/* -------------------------------------------------------------- */

/* ----- Set up login and security ----- */
EXEC sp_addlinkedsrvlogin 
    @rmtsrvname = 'LibraryName',
    @useself = 'false',
    @locallogin = NULL,
    @rmtuser = 'ReadOnlyUser',
    @rmtpassword = 'P455W0RD'

/* -------------------------------------------------------------- */

/* ----- Drop an existing linked server ----- */
EXEC sys.sp_dropserver 
    @server = N'LibraryName',
    @droplogins = 'droplogins';

/* -------------------------------------------------------------- */

/* Add the server into a custom table to manage remote connections */

INSERT INTO
	FourFarthings.Lss.RemoteConnections
		(LibraryName,
		ServerID,
		ServerName,
		DataSource,
		RemoteUser)
VALUES
	('LibraryName',
	3,
	'LibName',
	'172.55.55.255,1433',
	'LIBSQL')