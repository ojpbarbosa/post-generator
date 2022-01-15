from colorama import init, Fore, Style

import os
from dotenv import load_dotenv

import json
import requests

from pathlib import Path

import time


def main():
    clear_command = "cls" if os.name == "windows" else "clear"
    os.system(clear_command)

    init(autoreset=True)

    load_dotenv()

    NEWSCATCHER_API_KEY = os.getenv("NEWSCATCHER_API_KEY")

    if NEWSCATCHER_API_KEY == "" or NEWSCATCHER_API_KEY == None:
        print(
            f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}NewsCatcher API key was not provided!\n")

    else:
        print(f"{Style.BRIGHT}\n\tType a {Fore.LIGHTGREEN_EX}keyword{Fore.RESET} to generate posts about it!")
        print(f"{Style.BRIGHT}\n\t{Fore.LIGHTYELLOW_EX}Keyword{Fore.LIGHTMAGENTA_EX}:{Fore.LIGHTGREEN_EX} ", end="")

        query = input()
        while query == "":
            print(f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}Invalid keyword!")
            print(
                f"{Style.BRIGHT}\t{Fore.LIGHTYELLOW_EX}Keyword{Fore.LIGHTMAGENTA_EX}:{Fore.LIGHTGREEN_EX} ", end="")
            query = input()

        print(f"{Style.BRIGHT}\n\tSelect a {Fore.LIGHTGREEN_EX}language!")

        print(
            f"{Style.BRIGHT}\n\t{Fore.LIGHTGREEN_EX}Available languages{Fore.LIGHTMAGENTA_EX}:\n")

        available_languages = ["🌍 Afrikaans", "👳 Arabic", "🇧🇬 Bulgarian", "🌏 Bengali", "🇪🇸 Catalan", "🇨🇿 Czech", "🇬🇧 Welsh", "🇨🇳 Chinese", "🇩🇰 Danish", "🇩🇪 German",
                               "🇬🇷 Greek", "🇺🇸 English", "🇪🇸 Spanish", "🇪🇪 Estonian", "🇮🇷 Farsi", "🇫🇮 Finnish", "🇫🇷 French", "🇬🇺 Guam", "🇮🇱 Hebrew", "🇮🇳 Hindi", "🇭🇷 Croatian",
                               "🇭🇺 Hungarian", "🇮🇩 Indonesian", "🇮🇹 Italian", "🇯🇵 Japanese", "🇰🇳 Saint Kitts and Nevis English", "🇰🇷 Korean", "🇱🇹 Lithuanian", "🇱🇻 Latvian",
                               "🇲🇰 Macedonian", "🇮🇳 Malayalam", "🇲🇷 Mauritian", "🇳🇬 Nigerian", "🇳🇱 Dutch", "🇳🇴 Norwegian", "🇵🇰 Punjabi", "🇵🇱 Polish", "🇵🇹 Portuguese", "🇷🇴 Romanian",
                               "🇷🇺 Russian", "🇸🇰 Slovak", "🇸🇮 Slovenian", "🇸🇴 Somali", "🇦🇱 Albanian", "🇸🇪 Swedish", "🇹🇭 Thai", "🇹🇱 Timor Portuguese and Tetum", "🇹🇳 Turkish", "🇹🇼 Taiwan Chinese",
                               "🇬🇧 British English", "🇵🇰 Urdu", "🇻🇳 Vietnamese"]

        for i in range(len(available_languages)):
            print(
                f"{Style.BRIGHT}\t\t{Fore.LIGHTYELLOW_EX}-{Fore.RESET} {available_languages[i]}{Fore.LIGHTMAGENTA_EX}")

        print(f"{Style.BRIGHT}\n\t{Fore.LIGHTYELLOW_EX}Language{Fore.LIGHTMAGENTA_EX}:{Fore.LIGHTGREEN_EX} ", end="")

        selected_language = input()
        while selected_language == "":
            print(
                f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}Invalid language!")
            print(
                f"{Style.BRIGHT}\t{Fore.LIGHTYELLOW_EX}Language{Fore.LIGHTMAGENTA_EX}:{Fore.LIGHTGREEN_EX} ", end="")
            selected_language = input()

        language_codes = ["af", "ar", "bg", "bn", "ca", "cs", "cy", "cn", "da", "de", "el", "en", "es", "et", "fa", "fi", "fr", "gu", "he", "hi", "hr", "hu", "id", "it", "ja", "kn",
                          "ko", "lt", "lv", "mk", "ml", "mr", "ne", "nl", "no", "pa", "pl", "pt", "ro", "ru", "sk", "sl", "so", "sq", "sv", "th", "tl", "tr", "tw", "uk", "ur", "vi"]

        language = ""
        emojized_language = ""
        for available_language in available_languages:
            if selected_language.lower() == available_language.lower()[2:].replace(" ", ""):
                language = language_codes[available_languages.index(
                    available_language)]
                emojized_language = available_language
                break

        while language == "":
            print(
                f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}Invalid language!")
            print(
                f"{Style.BRIGHT}\t{Fore.LIGHTYELLOW_EX}Language{Fore.LIGHTMAGENTA_EX}:{Fore.LIGHTGREEN_EX} ", end="")

            selected_language = input()

            for available_language in available_languages:
                if selected_language.lower() == available_language.lower()[2:].replace(" ", ""):
                    language = language_codes[available_languages.index(
                        available_language)]
                    emojized_language = available_language
                    break

        print(f"{Style.BRIGHT}\n\tHit {Fore.LIGHTGREEN_EX}[ ENTER ]{Fore.RESET} to search for articles about {Fore.LIGHTYELLOW_EX}" + f'"{query}"' + f"{Fore.RESET} in {emojized_language} or hit {Fore.LIGHTRED_EX}[ CTRL + C ]{Fore.RESET} to abort." +
              f"\n\t{Fore.LIGHTRED_EX}* Note{Fore.LIGHTMAGENTA_EX}:{Fore.RESET} This might take a few seconds.\n\t", end="")

        proceed = None
        try:
            proceed = True if input() == "" else False
        except:
            proceed = False

        if proceed:
            response = requests.get(
                "https://api.newscatcherapi.com/v2/search",
                headers={
                    "x-api-key": f"{NEWSCATCHER_API_KEY}"
                },
                params={
                    "q": query.replace(" ", "-").lower(),
                    "lang": language,
                },
            ).json()

            if response["status"] == "ok":
                articles = response["articles"]

                posts = []
                for article in articles:
                    post = {
                        "title": article["title"],
                        "content": article["summary"].replace("\n", " ").replace("  ", " "),
                        "image": article["media"],
                        "author": article["author"],
                        "created_at": article["published_date"],
                    }

                    posts.append(post)

                print(f"{Style.BRIGHT}\t{Fore.LIGHTYELLOW_EX}" + str(len(
                    response["articles"])) + f" articles{Fore.RESET} about {Fore.LIGHTYELLOW_EX}" + f'"{query}"' + f"{Fore.LIGHTGREEN_EX} were found and transformed into posts.")
                print(
                    f"{Style.BRIGHT}\tDo you want them to be printed? {Fore.LIGHTGREEN_EX}(yes) {Fore.RESET}", end="")
                print_proceed_answer = input()

                while print_proceed_answer != "" and print_proceed_answer != "yes" and print_proceed_answer != "y" and print_proceed_answer != "no" and print_proceed_answer != "n":
                    print(f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}Invalid option!{Fore.RESET} Existent options: {Fore.LIGHTYELLOW_EX}yes (default){Fore.RESET}, {Fore.LIGHTYELLOW_EX}y{Fore.RESET}, {Fore.LIGHTYELLOW_EX}no{Fore.RESET} and {Fore.LIGHTYELLOW_EX}n{Fore.RESET}.")
                    print(
                        f"{Style.BRIGHT}\tDo you want them to be printed? {Fore.LIGHTGREEN_EX}(yes) {Fore.RESET}", end="")
                    print_proceed_answer = input()

                print_proceed = True if print_proceed_answer == "" or print_proceed_answer == "yes" or print_proceed_answer == "y" else False

                if print_proceed:
                    for post in posts:
                        print(f"""{Style.BRIGHT}\n\t{Fore.LIGHTYELLOW_EX}> POST <\n
                            {Fore.LIGHTGREEN_EX}- Title{Fore.LIGHTYELLOW_EX}: {Fore.RESET}{post["title"]}
                            {Fore.LIGHTGREEN_EX}- Content{Fore.LIGHTYELLOW_EX}: {Fore.RESET}{post["content"]}
                            {Fore.LIGHTGREEN_EX}- Image{Fore.LIGHTYELLOW_EX}: {Fore.RESET}{post["image"]}
                            {Fore.LIGHTGREEN_EX}- Author{Fore.LIGHTYELLOW_EX}: {Fore.RESET}{post["author"]}
                            {Fore.LIGHTGREEN_EX}- Created at{Fore.LIGHTYELLOW_EX}: {Fore.RESET}{post["created_at"]}
                        """)

                print(
                    f"{Style.BRIGHT}\n\tSave posts locally? {Fore.LIGHTGREEN_EX}(yes) {Fore.RESET}", end="")
                save_posts = input()

                while save_posts != "" and save_posts != "yes" and save_posts != "y" and save_posts != "no" and save_posts != "n":
                    print(f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}Invalid option!{Fore.RESET} Existent options: {Fore.LIGHTYELLOW_EX}yes (default){Fore.RESET}, {Fore.LIGHTYELLOW_EX}y{Fore.RESET}, {Fore.LIGHTYELLOW_EX}no{Fore.RESET} and {Fore.LIGHTYELLOW_EX}n{Fore.RESET}.")
                    print(
                        f"{Style.BRIGHT}\n\tSave posts locally? {Fore.LIGHTGREEN_EX}(yes) {Fore.RESET}", end="")

                    save_posts = input()

                save_posts = True if save_posts == "" or save_posts == "yes" or save_posts == "y" else False

                if save_posts:
                    data = {"posts": posts}

                    Path(Path.cwd() / "posts").mkdir(parents=True, exist_ok=True)

                    with open(f"posts/{str(time.time()).split('.')[0]}-{query.replace(' ', '-')}.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    f.close()

                print(
                    f"{Style.BRIGHT}\n\tPush posts to your API? {Fore.LIGHTGREEN_EX}(yes) {Fore.RESET}", end="")
                push_posts = input()

                while push_posts != "" and push_posts != "yes" and push_posts != "y" and push_posts != "no" and push_posts != "n":
                    print(f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}Invalid option!{Fore.RESET} Existent options: {Fore.LIGHTYELLOW_EX}yes (default){Fore.RESET}, {Fore.LIGHTYELLOW_EX}y{Fore.RESET}, {Fore.LIGHTYELLOW_EX}no{Fore.RESET} and {Fore.LIGHTYELLOW_EX}n{Fore.RESET}.")
                    print(
                        f"{Style.BRIGHT}\n\tPush posts to your API? {Fore.LIGHTGREEN_EX}(yes) {Fore.RESET}", end="")

                    push_posts = input()

                push_posts = True if push_posts == "" or push_posts == "yes" or push_posts == "y" else False

                if push_posts:
                    post_structure = """
                    {
                        "title": string,
                        "content": string,
                        "image": string,
                        "author": object,
                        "created_at": Date
                    }
                    """

                    print(f"{Style.BRIGHT}\n\tTo push the posts to your API, you need to have an {Fore.LIGHTYELLOW_EX}endpoint{Fore.RESET} where the posts can be pushed acording with the structure:\n{Fore.LIGHTBLUE_EX}{post_structure}")
                    print(f"{Style.BRIGHT}\n\t{Fore.LIGHTYELLOW_EX}API's URL and endpoint{Fore.LIGHTMAGENTA_EX}: {Fore.LIGHTGREEN_EX}(e.g. https://myapi.com/posts/generated) {Fore.RESET}", end="")

                    url = input()

                    while url == "":
                        print(f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}Invalid URL and endpoint!{Fore.LIGHTYELLOW_EX}\n\ttAPI's URL and endpoint{Fore.LIGHTMAGENTA_EX}: {Fore.LIGHTGREEN_EX}(e.g. https://myapi.com/posts/generated) {Fore.RESET}", end="")

                        url = input()

                    try:
                        for post in posts:
                            requests.post(url, data={
                                "title": post["title"],
                                "content": post["content"],
                                "image": post["image"],
                                "author": post["author"],
                                "created_at": post["created_at"]
                            })

                        print(f"{Style.BRIGHT}\n\tThe posts about {Fore.LIGHTYELLOW_EX}" + f'"{query}"' +
                              f"{Fore.RESET} were {Fore.LIGHTGREEN_EX}successfully pushed to your API!")
                    except Exception as err:
                        print(f"{Style.BRIGHT}\n\tAn {Fore.LIGHTRED_EX}error{Fore.RESET} occurred while pushing the posts to your API!\n\tError message{Fore.LIGHTMAGENTA_EX}: {Fore.LIGHTYELLOW_EX}" + f'"{err}"')

            elif response["status"] == "error":
                print(f"{Style.BRIGHT}\tAn {Fore.LIGHTRED_EX}error{Fore.RESET} occurred while generating posts.\n\tError message{Fore.LIGHTMAGENTA_EX}: {Fore.LIGHTYELLOW_EX}" +
                      f'"{response["message"]}"')

            else:
                print(f"{Style.BRIGHT}\t{Fore.LIGHTRED_EX}No articles{Fore.RESET} about {Fore.LIGHTYELLOW_EX}" +
                      f'"{query}"' + f"{Fore.RESET} could be found!")


if __name__ == "__main__":
    main()
