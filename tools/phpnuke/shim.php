<?php
// Environment shim for PHP-Nuke 7.1 on PHP 5.6: chains the museum legacy shim and
// restores import_request_variables() (removed in PHP 5.4), which mainfile.php calls.
require '/usr/local/lib/php-legacy-shim.php';
if (!function_exists('import_request_variables')) {
    function import_request_variables($types, $prefix = '') {
        $map = array('g' => $_GET, 'p' => $_POST, 'c' => $_COOKIE);
        foreach (str_split(strtolower($types)) as $t) {
            if (!isset($map[$t])) continue;
            foreach ($map[$t] as $k => $v) { $GLOBALS[$prefix . $k] = $v; }
        }
        return true;
    }
}
