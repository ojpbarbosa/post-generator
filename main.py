from colorama import init, Fore, Style

import os
from dotenv import load_dotenv

import json
import requests

from pathlib import Path


os.system("cls")
init(autoreset=True)

print(f"{Style.BRIGHT}\n\tType a {Fore.LIGHTGREEN_EX}keyword{Fore.RESET} to generate posts about it!")
print(f"{Style.BRIGHT}\n\t{Fore.LIGHTYELLOW_EX}Keyword{Fore.LIGHTMAGENTA_EX}:{Fore.LIGHTGREEN_EX} ", end="")

query = input()
while query == "":
  print(f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}Invalid keyword{Fore.RESET}!")
  print(f"{Style.BRIGHT}\t{Fore.LIGHTYELLOW_EX}Keyword{Fore.LIGHTMAGENTA_EX}:{Fore.LIGHTGREEN_EX} ", end="")
  query = input()

print(f"{Style.BRIGHT}\n\tType {Fore.LIGHTGREEN_EX}[ ENTER ]{Fore.RESET} to search for articles about {Fore.LIGHTYELLOW_EX}" + f'"{query}"' + f"{Fore.RESET}." +
      f"\n\t{Fore.LIGHTRED_EX}* Note{Fore.LIGHTMAGENTA_EX}:{Fore.RESET} This might take a few seconds.", end="")

proceed = True if input() == "" else False

if proceed:
  load_dotenv()

  response = requests.get(
    "https://api.newscatcherapi.com/v2/search",
    headers = {
      "x-api-key": os.getenv("NEWSCATCHER_API_KEY")
    },
    params = {
      "q": query.replace(" ", "-").lower(),
      "lang": "en",
      "sort_by": "relevancy",
      "page": "1"
    },
  ).json()

  if response["status"] == "ok":
    articles = response["articles"]

    posts = []
    for article in articles:
      title = article["title"]
      image = article["media"]
      content = article["summary"].replace("\n", " ").replace("  ", " ")
      votes = article["rank"]
      author = article["author"]
      date = article["published_date"]

      post = {
        "author": author,
        "content": content,
        "community": query.lower(),
        "date": date,
        "image": image,
        "title": title,
        "votes": votes
      }

      posts.append(post)

    data = { "posts": posts }

    Path(Path.cwd() / "posts").mkdir(parents=True, exist_ok=True)

    with open("posts/" + query.replace(" ", "-") + ".json", "w", encoding="utf-8") as f:
      json.dump(data, f, ensure_ascii=False, indent=2)
    f.close()

    print(f"{Style.BRIGHT}\n\t{Fore.LIGHTYELLOW_EX}" + str(len(response["articles"])) + f" articles{Fore.RESET} about {Fore.LIGHTYELLOW_EX}" + f'"{query}"' + f"{Fore.LIGHTGREEN_EX} were found and transformed into posts{Fore.RESET}.")
    print(f"{Style.BRIGHT}\tDo you want them to be printed? {Fore.LIGHTGREEN_EX}(yes) {Fore.RESET}", end="")
    print_proceed_answer = input()

    while print_proceed_answer != "" and print_proceed_answer != "yes" and print_proceed_answer != "y" and print_proceed_answer != "no" and print_proceed_answer != "n":
      print(f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}Invalid option{Fore.RESET}! Existent options: {Fore.LIGHTYELLOW_EX}yes{Fore.RESET} (default), {Fore.LIGHTYELLOW_EX}y{Fore.RESET}, {Fore.LIGHTYELLOW_EX}no{Fore.RESET} and {Fore.LIGHTYELLOW_EX}n{Fore.RESET}.")
      print(f"{Style.BRIGHT}\tDo you want them to be printed? {Fore.LIGHTGREEN_EX}(yes) {Fore.RESET}", end="")
      print_proceed_answer = input()

    print_proceed = True if print_proceed_answer == "" or print_proceed_answer == "yes" or print_proceed_answer == "y" else False

    if print_proceed:
      data_posts = None

      with open("posts/" + query.replace(" ", "-").lower() + ".json", "r", encoding="utf-8") as f:
        data_posts = json.load(f)
      f.close()

      for data_post in data_posts["posts"]:
        print(f"""{Style.BRIGHT}\n\t{Fore.LIGHTYELLOW_EX}> POST <\n
          {Fore.LIGHTGREEN_EX}- Title{Fore.LIGHTYELLOW_EX}: {Fore.RESET}{data_post["title"]}
          {Fore.LIGHTGREEN_EX}- Content{Fore.LIGHTYELLOW_EX}: {Fore.RESET}{data_post["content"]}
          {Fore.LIGHTGREEN_EX}- Author{Fore.LIGHTYELLOW_EX}: {Fore.RESET}{data_post["author"]}
          {Fore.LIGHTGREEN_EX}- Votes{Fore.LIGHTYELLOW_EX}: {Fore.RESET}{data_post["votes"]}
          {Fore.LIGHTGREEN_EX}- Image{Fore.LIGHTYELLOW_EX}: {Fore.RESET}{data_post["image"]}
          {Fore.LIGHTGREEN_EX}- Date{Fore.LIGHTYELLOW_EX}: {Fore.RESET}{data_post["date"]}
        """)

    print(f"{Style.BRIGHT}\n\tSave generated posts to FastLearn API? {Fore.LIGHTGREEN_EX}(yes) {Fore.RESET}", end="")
    save_generated_posts = input()

    while save_generated_posts != "" and save_generated_posts != "yes" and save_generated_posts != "y" and save_generated_posts != "no" and save_generated_posts != "n":
      print(f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}Invalid option{Fore.RESET}! Existent options: {Fore.LIGHTYELLOW_EX}yes{Fore.RESET} (default), {Fore.LIGHTYELLOW_EX}y{Fore.RESET}, {Fore.LIGHTYELLOW_EX}no{Fore.RESET} and {Fore.LIGHTYELLOW_EX}n{Fore.RESET}.")
      print(f"{Style.BRIGHT}\n\tSave generated posts to FastLearn API? {Fore.LIGHTGREEN_EX}(yes) {Fore.RESET}", end="")

      save_generated_posts = input()

    save_generated_posts = True if save_generated_posts == "" or save_generated_posts == "yes" or save_generated_posts == "y" else False

    if save_generated_posts:
      # requests.post(
      #   "https://fastlearn-api.herokuapp.com/post/generator",
      #   headers = {
      #     "authorization":
      #   },
      #   data = {
      #     "posts": posts
      #   },
      # )

      print(f"{Style.BRIGHT}\n\tThe posts about {Fore.LIGHTYELLOW_EX}" + f'"{query}"' + f"{Fore.RESET} were {Fore.LIGHTGREEN_EX}successfully saved{Fore.RESET}!")

  else:
    print(f"{Style.BRIGHT}\n\t{Fore.LIGHTRED_EX}No articles{Fore.RESET} about {Fore.LIGHTYELLOW_EX}" + f'"{query}"' + f"{Fore.RESET} could be found!")