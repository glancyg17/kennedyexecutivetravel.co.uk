# Over-9-passenger visibility switch (temporary, pending operator licence)

    python3 tools/16-seater/toggle.py status
    python3 tools/16-seater/toggle.py hide
    python3 tools/16-seater/toggle.py show      # once the licence is granted

Hides/restores DISPLAY content for any vehicle carrying more than 9 passengers:
the 12-14 seat minibus and Ford Transit 17-seater (group, fleet, home, services,
executive pages), the airport-prices Minibus tier (its first row is 9-10 pax), the
meta descriptions and llms.txt. Remaining copy refers to the 8-seat mini bus only.

NOT touched: booking form dropdowns / passenger-count selects, and the dispatch app.
Commit after running either command, then deploy. Folder is excluded via .assetsignore.
