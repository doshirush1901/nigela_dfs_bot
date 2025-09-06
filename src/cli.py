import argparse, asyncio
from datetime import date, timedelta, datetime
from .suggest import suggest_for_day
from .cards import generate_cook_cards_pdf
from .io_xls import write_dishes
from .parse_url import url_to_dishes
from .parse_pdf import pdf_to_dishes
from .parse_image import image_to_dishes
from .ingest_api import spoonacular_search, edamam_search, map_spoonacular, map_edamam
from .ebooks import discover_free_cookbooks, fetch_ebooks
from .ebooks_ingest import ingest_manifest_to_dishes
from .emailer import send_menu_email
from .youtube_integration import YouTubeVideoFinder, enhance_recipes_with_videos

def print_plan(plan: dict):
    for meal, slots in plan.items():
        print(f"\n=== {meal.upper()} ===")
        for slot, dish in slots.items():
            print(f"- {slot}: {dish.name}")
            if dish.variant_adults: print(f"  Adults: {dish.variant_adults}")
            if dish.variant_kids:   print(f"  Kids  : {dish.variant_kids}")

def _resolve_date(arg: str) -> date:
    arg = arg.strip().lower()
    if arg in ("today",): return date.today()
    if arg in ("tomorrow","tmrw"): return date.today() + timedelta(days=1)
    return date.fromisoformat(arg)

def main():
    ap = argparse.ArgumentParser("nigela")
    sub = ap.add_subparsers(dest="cmd")

    s1 = sub.add_parser("suggest"); s1.add_argument("--date", required=True)
    s2 = sub.add_parser("cards");   s2.add_argument("--date", required=True); s2.add_argument("--out", required=True)
    em = sub.add_parser("email");   em.add_argument("--for", dest="for_date", required=True, help="'today'|'tomorrow'|YYYY-MM-DD")

    iu = sub.add_parser("ingest-url"); iu.add_argument("--url", required=True); iu.add_argument("--meal", default="dinner"); iu.add_argument("--slot", default=None); iu.add_argument("--cuisine", default=None)
    ip = sub.add_parser("ingest-pdf"); ip.add_argument("--file", required=True); ip.add_argument("--meal", default="dinner"); ip.add_argument("--cuisine", default=None)
    ii = sub.add_parser("ingest-image"); ii.add_argument("--file", required=True); ii.add_argument("--cuisine", default=None)

    ia = sub.add_parser("ingest-api"); ia.add_argument("--provider", choices=["spoonacular","edamam"], required=True); ia.add_argument("--query", required=True); ia.add_argument("--meal", default="dinner"); ia.add_argument("--slot", default=None); ia.add_argument("--cuisine", default=None); ia.add_argument("--n", type=int, default=5)

    es = sub.add_parser("ebooks-search"); es.add_argument("--max", type=int, default=20); es.add_argument("--cuisines", default="gujarati,rajasthani,himachali,kerala,tamil,goan,italian,mexican,japanese,burmese,indian chinese"); es.add_argument("--diet", default="jain,vegetarian,eggless,satvik")
    ed = sub.add_parser("ebooks-download"); ed.add_argument("--max", type=int, default=20); ed.add_argument("--out", default="library/ebooks"); ed.add_argument("--cuisines", default="gujarati,rajasthani,himachali,kerala,tamil,goan,italian,mexican,japanese,burmese,indian chinese"); ed.add_argument("--diet", default="jain,vegetarian,eggless,satvik")
    ei = sub.add_parser("ebooks-ingest"); ei.add_argument("--manifest", default="library/ebooks/manifest.json"); ei.add_argument("--data-dir", default="data"); ei.add_argument("--max-books", type=int, default=20); ei.add_argument("--max-lines", type=int, default=12000)

    # YouTube video enhancement
    yv = sub.add_parser("enhance-videos"); yv.add_argument("--data-dir", default="data"); yv.add_argument("--max-recipes", type=int, default=20)

    args = ap.parse_args()
    if args.cmd == "suggest":
        d = _resolve_date(args.date)
        plan = suggest_for_day(d)
        print_plan(plan)
    elif args.cmd == "cards":
        d = _resolve_date(args.date)
        pdf = generate_cook_cards_pdf(d, dishes=None)  # pass explicit dishes list if you want
        with open(args.out, "wb") as f: f.write(pdf.read())
        print(f"Saved {args.out}")
    elif args.cmd == "email":
        d = _resolve_date(args.for_date)
        plan = suggest_for_day(d)
        sent = send_menu_email(plan, d.isoformat())
        if not sent: print("Email not sent; check SMTP env vars.")
    elif args.cmd == "ingest-url":
        dishes = asyncio.run(url_to_dishes(args.url, meal_hint=args.meal, cuisine_hint=args.cuisine))
        if args.slot:
            for d in dishes: d.tags.append(f"{args.meal}:{args.slot}")
        n = write_dishes("data/dishes.xlsx", dishes)
        print(f"Added {n} dishes from URL")
    elif args.cmd == "ingest-pdf":
        dishes = pdf_to_dishes(args.file, meal_hint=args.meal, cuisine_hint=args.cuisine)
        n = write_dishes("data/dishes.xlsx", dishes)
        print(f"Added {n} dishes from PDF")
    elif args.cmd == "ingest-image":
        dishes = image_to_dishes(args.file, cuisine_hint=args.cuisine)
        n = write_dishes("data/dishes.xlsx", dishes)
        print(f"Added {n} dishes from image OCR")
    elif args.cmd == "ingest-api":
        if args.provider == "spoonacular":
            items = asyncio.run(spoonacular_search(args.query, number=args.n))
            dishes = map_spoonacular(items, meal_hint=args.meal, cuisine_hint=args.cuisine)
        else:
            items = asyncio.run(edamam_search(args.query, number=args.n))
            dishes = map_edamam(items, meal_hint=args.meal, cuisine_hint=args.cuisine)
        if args.slot:
            for d in dishes: d.tags.append(f"{args.meal}:{args.slot}")
        n = write_dishes("data/dishes.xlsx", dishes)
        print(f"Added {n} dishes from {args.provider}")
    elif args.cmd == "ebooks-search":
        prefs = {"cuisines":[s.strip() for s in args.cuisines.split(",") if s.strip()],
                 "diet_terms":[s.strip() for s in args.diet.split(",") if s.strip()]}
        items = asyncio.run(discover_free_cookbooks(prefs, max_total=args.max))
        for i, it in enumerate(items, 1):
            print(f"{i:02d}. {it.get('title','(untitled)')}  -> {it['url']}")
    elif args.cmd == "ebooks-download":
        prefs = {"cuisines":[s.strip() for s in args.cuisines.split(",") if s.strip()],
                 "diet_terms":[s.strip() for s in args.diet.split(",") if s.strip()]}
        results = fetch_ebooks(prefs, out_dir=args.out, max_total=args.max)
        for r in results: print(f"Saved: {r['title']}  -> {r['path']}")
        print(f"\nManifest written to {args.out}/manifest.json")
    elif args.cmd == "ebooks-ingest":
        added = ingest_manifest_to_dishes(args.manifest, data_dir=args.data_dir, max_books=args.max_books, max_lines=args.max_lines)
        print(f"Added {added} dishes into {args.data_dir}/dishes.xlsx")
    elif args.cmd == "enhance-videos":
        from .io_xls import read_dishes, write_dishes
        import asyncio
        
        print(f"🎥 Enhancing recipes with YouTube videos...")
        dishes = read_dishes(f"{args.data_dir}/dishes.xlsx")[:args.max_recipes]
        
        # Add video links to recipes
        enhanced_dishes = asyncio.run(enhance_recipes_with_videos(dishes))
        
        # Update database with video links (would need to extend Excel schema)
        print(f"✅ Enhanced {len(enhanced_dishes)} recipes with video links")
        
        # Show results
        for dish in enhanced_dishes:
            if hasattr(dish, 'video_url') and dish.video_url:
                print(f"🎥 {dish.name} → {dish.video_url}")
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
