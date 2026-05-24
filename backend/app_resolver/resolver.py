from .scanner import find_executables
from .scorer import score_exe
from .recents import load_recents, save_recents
from .special_apps import handle_special_app
from .web_apps import handle_web_app
from .aliases import handle_alias
from .shortcut_scanner import scan_shortcuts

recent_apps = load_recents()

ALIASES = {
    "vs code": "code",
    "vscode": "code",
    "visual studio code": "code"
}

def normalize(app_name):
    return ALIASES.get(app_name.lower(), app_name.lower())

def resolve_app(app_name):
    app_name = normalize(app_name)

    # 🔥 1. Recents
    if app_name in recent_apps:
        print(f"⚡ Found in recents: {recent_apps[app_name]}")
        return ("exe", recent_apps[app_name])

    # 🔥 2. Alias apps (ChatGPT, Terminal, etc.)
    if handle_alias(app_name):
        return ("alias", None)

    # 🔥 3. Special apps (UWP / system)
    if handle_special_app(app_name):
        return ("special", None)

    # 🔥 4. Web apps
    if handle_web_app(app_name):
        return ("web", None)
    
    # 🔥 5. Shortcut scan (Start Menu + Desktop)
    shortcut_candidates = scan_shortcuts(app_name)

    if shortcut_candidates:
        print("\n🔗 Shortcut matches:")

        import os

        valid_targets = [
            target for _, target in shortcut_candidates
            if target and target.endswith(".exe") and os.path.exists(target)
        ]

        if valid_targets:
            scored = [(t, score_exe(t, app_name)) for t in valid_targets]
            scored.sort(key=lambda x: x[1], reverse=True)

            for t, s in scored[:5]:
                print(f"{s:.1f} → {t}")

            best_target = scored[0][0]

            recent_apps[app_name] = best_target
            save_recents(recent_apps)

            print(f"\n✅ Selected (shortcut): {best_target}")
            return ("exe", best_target)

    # 🔥 6. EXE heuristic scan
    candidates = find_executables(app_name)

    if not candidates:
        print("❌ No candidates found")
        return (None, None)

    scored = [(p, score_exe(p, app_name)) for p in candidates]
    scored.sort(key=lambda x: x[1], reverse=True)

    print("\n🔍 Top candidates:")
    for p, s in scored[:5]:
        print(f"{s:.1f} → {p}")

    best_path = scored[0][0]

    # Save to recents
    recent_apps[app_name] = best_path
    save_recents(recent_apps)

    print(f"\n✅ Selected: {best_path}")

    return ("exe", best_path)