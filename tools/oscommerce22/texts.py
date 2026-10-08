#!/usr/bin/env python3
"""Store texts a 2004 shop owner would edit with osCommerce's Tools > Define Languages
(admin/define_language.php rewrites these define() lines in includes/languages/english/).

usage: texts.py <catalog dir>
"""
import re
import sys

CAT = sys.argv[1]
EDITS = {
    'includes/languages/english.php': {
        'TITLE': 'TechBits Computer Accessories',
    },
    'includes/languages/english/index.php': {
        'TEXT_MAIN': 'Welcome to <b>TechBits Computer Accessories</b>! We stock mice, keyboards, sound cards, '
                     'graphics cards, memory, DVD writers, flash drives and networking gear from Logitech, Microsoft, '
                     'Creative, ATI, SanDisk, Netgear and more.<br><br>'
                     'Orders placed before 3pm Eastern ship the same day. Shipping is a flat $5.00 anywhere in the '
                     'continental US. Local customers are welcome to pick up their order at our store on Kennedy Blvd '
                     'in Tampa, Monday to Saturday, 10am to 7pm.<br><br>'
                     'Have a question about what will work with your computer? Use the <b>Contact Us</b> page or call '
                     'us at (813) 555-0142.',
    },
    'includes/languages/english/shipping.php': {
        'TEXT_INFORMATION': '<b>Shipping</b><br>All orders ship by UPS Ground from Tampa, Florida. Shipping is a flat '
                            '$5.00 per order within the continental US. Orders placed before 3pm Eastern time on a '
                            'business day ship the same day. You will receive an e-mail when your order ships.<br><br>'
                            '<b>Returns</b><br>Unopened items can be returned within 30 days for a full refund. '
                            'Defective items are exchanged within 30 days; after that please contact the manufacturer. '
                            'Opened software and memory cards cannot be returned unless defective. Please call or e-mail '
                            'us for a return authorization number before sending anything back.',
    },
    'includes/languages/english/privacy.php': {
        'TEXT_INFORMATION': 'We use the information you give us only to process your orders and, if you ask for it, '
                            'to send you our newsletter. We never sell or rent your name, address or e-mail address '
                            'to anyone.<br><br>Credit card numbers are used only for the order they were given for. '
                            'This site uses a cookie to remember the contents of your shopping cart.',
    },
    'includes/languages/english/conditions.php': {
        'TEXT_INFORMATION': 'Prices and availability are subject to change without notice. We do our best to keep the '
                            'information on this site accurate, but we are not responsible for typographical errors. '
                            'Product names and logos are trademarks of their respective owners. All sales are subject '
                            'to our Shipping &amp; Returns policy. Florida residents pay 7% sales tax.',
    },
}

for rel, defs in EDITS.items():
    path = CAT + '/' + rel
    src = open(path, encoding='latin-1').read()
    for name, text in defs.items():
        lit = "'" + text.replace('\\', '\\\\').replace("'", "\\'") + "'"
        # the whole define() statement; it sits on one line (TEXT_MAIN concatenates tep_href_link() calls)
        src, n = re.subn(r"^define\('%s',.*\);[ \t]*$" % name,
                         lambda m: "define('%s', %s);" % (name, lit), src, count=1, flags=re.M)
        assert n == 1, (rel, name)
    open(path, 'w', encoding='latin-1').write(src)
