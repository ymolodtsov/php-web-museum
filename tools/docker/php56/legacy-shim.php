<?php
// Opt-in emulation of PHP 4-era behaviour for 2002-2005 apps (auto_prepend_file).
foreach (array('HTTP_GET_VARS' => '_GET', 'HTTP_POST_VARS' => '_POST', 'HTTP_COOKIE_VARS' => '_COOKIE',
               'HTTP_SERVER_VARS' => '_SERVER', 'HTTP_ENV_VARS' => '_ENV', 'HTTP_POST_FILES' => '_FILES') as $old => $new) {
    $GLOBALS[$old] = &$GLOBALS[$new];
}
if (getenv('MUSEUM_REGISTER_GLOBALS')) {
    foreach (array($_ENV, $_GET, $_POST, $_COOKIE, $_SERVER) as $src) {
        foreach ($src as $k => $v) { if (!isset($GLOBALS[$k])) { $GLOBALS[$k] = $v; } }
    }
}
if (!function_exists('session_register')) {
    function session_register() {
        foreach (func_get_args() as $n) { if (!isset($_SESSION[$n])) { $_SESSION[$n] = isset($GLOBALS[$n]) ? $GLOBALS[$n] : null; } $GLOBALS[$n] = &$_SESSION[$n]; }
        return true;
    }
    function session_is_registered($n) { return isset($_SESSION[$n]); }
    function session_unregister($n) { unset($_SESSION[$n]); return true; }
}
