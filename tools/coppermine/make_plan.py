#!/usr/bin/env python3
"""Build photos.json (per-photo plan) from sources.json plus the gallery's content.

usage: make_plan.py  (writes photos.json next to this script)
Fields: folder, file, name, title, caption, aspect, camera, taken, edited,
exposure, fnumber, focal, iso, flash, hits, votes (list of 1-5), comments.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = {s["name"]: s for s in json.load(open(os.path.join(HERE, "sources.json")))}

# name, title, caption, taken, exposure, f, focal, iso, flash, hits, votes
ALBUMS = [
 ("newengland", "2004:10:17 22:05:00", "Adobe Photoshop Elements 3.0", [
  ("green_mountains", "Green Mountains at Sunrise", "Frost on the car, mist on the river, and the hills lit up orange for about ten minutes. Route 100, Vermont.", "2004:10:08 07:12:41", "1/125", 8, 35, 200, 16, 287, [5, 5, 4, 5]),
  ("white_mountains", "Kancamagus Highway", "Pulled over at every single overlook on the Kancamagus. This was the best of them.", "2004:10:10 13:48:09", "1/500", 5.6, 5.4, 0, 24, 198, [4, 4]),
  ("eagle_lake", "Eagle Lake, Acadia", "Eagle Lake from the carriage road. Peak colour was a week earlier, but nobody told the maples by the water.", "2004:10:12 10:31:55", "1/200", 9, 24, 100, 16, 173, [5, 4]),
  ("acadia_birches", "Birches, Acadia", "", "2004:10:12 15:02:17", "1/60", 5.6, 41, 400, 16, 96, []),
  ("gorham_mountain", "View from Gorham Mountain", "Short climb, huge view. Otter Cliff and the ocean on the left.", "2004:10:13 11:20:38", "1/320", 10, 18, 100, 16, 141, [4]),
 ]),
 ("alps", "2004:09:04 19:40:00", "Adobe Photoshop Elements 2.0", [
  ("zermatt_stbernard", "Zermatt Mascot", "Every shop on the Bahnhofstrasse seems to have one of these parked outside. He did not move once in twenty minutes.", "2004:08:14 17:26:03", "1/250", 4.0, 9.7, 0, 24, 312, [5, 4, 5]),
  ("matterhorn_gornergrat", "Matterhorn from Gornergrat", "First train up, 7am. Worth every franc of the ridiculous ticket price.", "2004:08:15 08:41:22", "1/640", 8.0, 16.2, 0, 24, 941, [5, 5, 5, 4, 5, 5]),
  ("matterhorn_flowers", "Alpine Flowers", "Lying on my stomach in a meadow above Riffelalp to get this one. Glad nobody I know walked past.", "2004:08:16 11:05:47", "1/400", 11, 18, 100, 16, 402, [5, 4, 4]),
  ("alpine_lake", "Lake above Zermatt", "One of the little lakes on the Five Lakes walk. Freezing, and yes, I went in up to my knees.", "2004:08:17 14:12:30", "1/250", 9, 22, 100, 16, 266, [4, 5]),
  ("rhone_glacier", "Rhone Glacier", "The Hotel Belvedere on the Furka Pass road, practically sitting on the ice. You can walk into a tunnel cut in the glacier for a few francs.", "2004:08:19 12:47:11", "1/320", 8, 30, 100, 16, 227, [4]),
  ("ridge_walk", "Ridge Walk, Carnic Alps", "Last day of the trip, on the Austrian-Italian border. Nine hours, two litres of water, zero regrets.", "2004:08:21 13:30:56", "1/500", 11, 20, 100, 16, 158, [5, 4]),
 ]),
 ("morocco", "2005:01:29 16:20:00", "Adobe Photoshop Elements 3.0", [
  ("jemaa_storytellers", "Jemaa el-Fnaa Storytellers", "Every evening the square fills up with storytellers, musicians, snake charmers and food stalls. Nobody seemed to mind the camera as long as you dropped a few dirhams in the hat.", "2004:12:26 17:52:14", "1/30", 2.8, 5.4, 0, 16, 384, [5, 4, 5]),
  ("souk_semmarine", "Souk Semmarine", "The main covered street into the souks. The light through the slats was the best thing about it.", "2004:12:27 11:16:40", "1/160", 6.3, 18, 200, 16, 205, [4, 4]),
  ("marrakech_storks", "Storks on the Wall", "Storks nest all along the walls of the Badi Palace. They clatter their beaks like castanets.", "2004:12:28 10:03:52", "1/800", 5.6, 55, 100, 16, 117, [4]),
  ("marrakech_door", "A Door in the Medina", "", "2004:12:28 15:44:09", "1/125", 8, 24, 100, 16, 88, []),
  ("chefchaouen", "Chefchaouen Rooftops", "Six hours on a CTM bus from Fes to get here. The whole town is painted blue and it is very quiet after Marrakech.", "2004:12:31 12:25:18", "1/400", 10, 18, 100, 16, 263, [5, 5]),
  ("fes_tannery", "Chouara Tannery, Fes", "They hand you a sprig of mint at the door for the smell. You need it.", "2005:01:02 10:58:33", "1/250", 8, 50, 200, 16, 349, [5, 4, 4]),
 ]),
 ("portugal", "2005:02:13 21:10:00", "Adobe Photoshop Elements 3.0", [
  ("porto_rabelos", "Rabelo Boats, Porto", "The old port wine boats moored in front of the lodges in Vila Nova de Gaia. Tasting tours every half hour, which explains the rest of the afternoon.", "2005:02:04 15:30:11", "1/640", 8.0, 7.3, 0, 24, 176, [4, 4]),
  ("lisbon_tram", "Tram, Lisbon", "The trams climb streets you would not want to walk up. Rua da Bica at dusk.", "2005:02:05 18:06:45", "1/15", 2.8, 5.4, 0, 16, 239, [5, 4]),
  ("belem_tower", "Belem Tower", "", "2005:02:06 12:21:02", "1/500", 9, 18, 100, 16, 152, [4]),
  ("monserrate_sintra", "Monserrate Palace, Sintra", "Less famous than the Pena Palace and twice as nice. We had the gardens almost to ourselves.", "2005:02:07 14:37:26", "1/400", 5.6, 8.1, 0, 24, 131, [5]),
  ("cabo_da_roca", "Cabo da Roca", "Westernmost point of mainland Europe. You can buy a certificate that says you were here. We did not.", "2005:02:08 16:02:59", "1/500", 8.0, 5.4, 0, 24, 219, [4, 5]),
  ("algarve_cliffs", "Cliffs near Sagres", "Western Algarve in February: wind, sun, surfers, and nobody else.", "2005:02:10 13:15:44", "1/640", 11, 24, 100, 16, 187, [4, 4, 5]),
 ]),
 ("tokyo", "2005:03:01 23:30:00", "Nikon Capture 4.2", [
  ("sensoji_night", "Senso-ji at Night", "Asakusa after the shops close. The temple stays lit up and the crowds disappear.", "2005:02:24 21:14:08", "4/1", 11, 18, 200, 0, 214, [5, 5, 4]),
  ("shinjuku_neon", "Shinjuku East Exit", "Rush hour outside Shinjuku station. The pedestrian lights change and about a thousand people cross at once.", "2005:02:25 18:22:37", "1/30", 2.8, 5.4, 0, 16, 306, [4, 5]),
  ("nishi_shinjuku", "Nishi-Shinjuku Towers", "From the free observation deck at the Metropolitan Government Building.", "2005:02:25 20:41:15", "1/8", 2.8, 5.4, 0, 16, 162, [4]),
  ("shibuya_street", "Shibuya Side Street", "Center Gai, just up from the big crossing. Karaoke, pachinko and a lot of noise.", "2005:02:26 22:05:49", "1/40", 3.5, 18, 800, 0, 251, [4, 4]),
  ("tokyo_tower", "Tokyo Tower", "Tokyo Tower from the 40th floor of the World Trade Center building in Hamamatsucho, tripod jammed against the glass.", "2005:02:27 19:48:22", "2/1", 8, 35, 200, 0, 288, [5, 5, 4]),
 ]),
 ("seasia", "2005:05:27 21:40:00", "Adobe Photoshop Elements 3.0", [
  ("bangkok_tuktuks", "Bangkok Tuk-Tuk", "Lined up outside a gem shop on Charoen Krung. Every driver had a cousin with a tailor's shop.", "2005:04:28 16:40:12", "1/250", 8, 24, 100, 16, 142, [4]),
  ("floating_market", "Floating Market, Bangkok", "Damnoen Saduak, two hours out of Bangkok. Get there before eight, before the tour buses.", "2005:04:29 07:58:31", "1/200", 6.3, 42, 200, 16, 212, [4, 4, 5]),
  ("chiang_mai_bazaar", "Chiang Mai Night Bazaar", "Bought far too many cushion covers here.", "2005:05:02 20:31:06", "1/15", 2.8, 5.4, 0, 16, 129, [4]),
  ("luang_prabang_market", "Luang Prabang Morning Market", "Up at 5:30 for the monks' alms round (no photos, it felt wrong), then breakfast wandering through the market.", "2005:05:06 06:52:18", "1/60", 5.6, 26, 400, 16, 301, [5, 4, 5]),
  ("angkor_sunrise", "Angkor Wat Sunrise", "Worth getting up at 4:30am for. Shot from the edge of the north reflecting pool with about two hundred other people.", "2005:05:10 05:47:12", "1/125", 8, 24, 100, 16, 318, [5, 5, 4, 5, 4, 5, 4, 3, 4, 3]),
  ("phnom_krom_market", "Siem Reap Market Stalls", "Phnom Krom, on the road down to the Tonle Sap floating villages.", "2005:05:11 14:26:50", "1/400", 9, 18, 100, 16, 88, [4]),
  ("phnom_penh_riverside", "Phnom Penh Riverside", "Sisowath Quay in the late afternoon heat. The FCC bar is a few doors down.", "2005:05:13 16:58:40", "1/250", 5.6, 5.4, 0, 24, 63, []),
  ("mekong_delta_boat", "Mekong Delta Boats", "Two days on boats around Ben Tre and Can Tho. Most of the delta seems to get around this way.", "2005:05:15 09:12:27", "1/320", 8, 35, 100, 16, 97, [4]),
  ("hoian_lantern_street", "Hoi An Lanterns", "It rained all afternoon and the lanterns in the old town came on early.", "2005:05:17 17:36:04", "1/60", 4.5, 20, 400, 16, 176, [5, 4]),
  ("halong_bay", "Halong Bay Limestone Cliffs", "Evening on the junk, anchored between the islands.", "2005:05:20 18:14:55", "1/80", 5.6, 30, 200, 16, 254, [5, 5, 4]),
  ("halong_deck", "Halong Bay, Feet Up", "Hard day at the office.", "2005:05:21 10:40:16", "1/500", 9, 18, 100, 16, 134, [5, 3]),
 ]),
]

# comments: name -> list of (author, date, text)
COMMENTS = {
 "angkor_sunrise": [
  ("backpacker_rae", "2005-05-29 09:14:00", "We were at the same spot about a month before you, same sunrise crowd by the reflecting pool. Still worth getting up at 4:30am for, every time."),
  ("tgoodwin", "2005-05-30 19:52:00", "Great exposure on this one. Did you meter off the sky or the towers? Mine all came out either blown out or too dark."),
  ("Dan", "2005-05-30 22:31:00", "Spot metered on the sky just left of the towers and let the rest go dark. Took about fifteen tries."),
  ("mariana_v", "2005-06-04 11:03:00", "Added to favourites. Putting this on the list for next year's trip, thank you for posting the whole album!"),
 ],
 "matterhorn_gornergrat": [
  ("Steffi", "2004-09-07 08:40:00", "Wow, you were lucky with the weather. We were up there in July and saw nothing but cloud."),
  ("pete_h", "2004-11-21 14:12:00", "Is this the A75? Amazing what those little cameras can do."),
 ],
 "fes_tannery": [
  ("tgoodwin", "2005-02-02 20:07:00", "I can smell this photo."),
 ],
 "halong_bay": [
  ("Jess", "2005-05-30 08:25:00", "Gorgeous. Which boat company did you use? The reviews online are all over the place."),
  ("Dan", "2005-05-30 22:40:00", "Booked it through our guesthouse in Hanoi for $38 each, one night on board. Food was fine, cabins were small, views were not."),
 ],
 "jemaa_storytellers": [
  ("mariana_v", "2005-02-01 13:30:00", "Love this. Did you try the snail soup?"),
 ],
 "sensoji_night": [
  ("kenji", "2005-03-04 00:18:00", "Nice night shot. Next time go to Asakusa early in the morning too, very different feeling."),
 ],
 "green_mountains": [
  ("Mum", "2004-10-20 18:02:00", "Beautiful! Can I have a print of this one for the kitchen?"),
 ],
 "luang_prabang_market": [
  ("backpacker_rae", "2005-06-02 17:45:00", "Luang Prabang was my favourite place in the whole region. Did you make it out to the Kuang Si falls?"),
 ],
}


def main():
    plan = []
    counters = {"300d": 1834, "a75": 4217, "d70": 1102}
    for folder, edited_at, software, photos in sorted(ALBUMS, key=lambda a: a[3][0][3]):
        for (name, title, caption, taken, exp, f, focal, iso, flash, hits, votes) in photos:
            s = SRC[name]
            ratio = s["w"] / s["h"]
            aspect = "4:3" if ratio < 1.4 else "3:2"
            if aspect == "4:3":
                camera = "a75"
            else:
                camera = "d70" if folder == "tokyo" else "300d"
            counters[camera] += 7 + (hits % 23)
            num = counters[camera]
            fname = ("DSC_%04d.JPG" if camera == "d70" else "IMG_%04d.JPG") % num
            size = None
            if False:
                size = [1600, 1200]
            plan.append(dict(
                folder=folder, file=fname, name=name, title=title, caption=caption,
                aspect=aspect, size=size, camera=camera, taken=taken,
                edited=(edited_at if aspect == "3:2" else None), software=software,
                exposure=exp, fnumber=f, focal=focal, iso=iso or None, flash=flash,
                hits=hits, votes=votes, comments=COMMENTS.get(name, []),
                source_page=s["page"], original_url=s["url"].split("?")[0],
                source_title=s["title"], author=s["artist"].strip(), licence=s["lic"],
                source_size=[s["w"], s["h"]]))
    json.dump(plan, open(os.path.join(HERE, "photos.json"), "w"), indent=1)
    print(len(plan), "photos")


if __name__ == "__main__":
    main()
