<?php
// Environment shim for PostNuke 0.750 on PHP 5.6: chains the museum legacy shim and writes the
// session before PHP tears down objects. PHP 4 called session write handlers while globals were
// still alive; PHP >= 5.0.5 destroys objects first, so PostNuke's DB-backed session handler finds
// its ADOdb connection gone and logins are never stored. Shutdown functions still run in time.
require '/usr/local/lib/php-legacy-shim.php';
register_shutdown_function('museum_session_write_close');
function museum_session_write_close() { if (session_id() !== '') { session_write_close(); } }
