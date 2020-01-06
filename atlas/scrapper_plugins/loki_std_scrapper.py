""" A basic offline scrapper for shows

This scrapper attempts to find show name, seasson nr and episode
nr based on the file name and its containing folder.
"""
import re

REGEX_TAGS       = re.compile(r"\(.*?\)|\[.*?\]|\.\w{3}$")
REGEX_SPACERS    = re.compile(r"\.|\-|\_")
REGEX_EPISODE_NR = re.compile(r"\ (?:Episode|episode|[sS]\d+\ ?[eE]|\d[Xx])\ ?(\d+)")
REGEX_SEASON_NR = re.compile(r"\ (?:Season|season|[sS])\ ?(\d+)\ ?")
REGEX_NAME      = re.compile(r".+?(?=[Ss]eason)|.+?(?=\ [Ss]\ ?\d)|.+?$")

def scrape(path):
    cleaned_path = clean_path(path)
    name = scrape_name(cleaned_path).strip()
    season = scrape_season_nr(cleaned_path).rjust(2,"0")
    episode = scrape_episode_nr(cleaned_path).rjust(2,"0")
    return [("std","name",name),("std","season",season),("std","episode",episode)]

def clean_path(path):
    clear_meta      = re.sub(REGEX_TAGS,"",path)
    normalize_spaces = re.sub(REGEX_SPACERS," ",clear_meta)
    path_split       = normalize_spaces.split("/")
    file_name = path_split[-1]
    dir_name = ""
    if len(path_split) > 1:
        dir_name = path_split[-2]
    return (dir_name,file_name)

def scrape_episode_nr(cleaned_path):
    delta = cleaned_path[1].replace(cleaned_path[0],"")
    episode = re.findall(REGEX_EPISODE_NR,delta)
    if not episode:
        episode = re.findall(r"\d+",delta)
        if not episode:
            return "0"
        else:
            return episode[-1]
    else:
        return episode[-1]

def scrape_season_nr(cleaned_path):
    season_from_dir = re.findall(REGEX_SEASON_NR,cleaned_path[0])
    if not season_from_dir:
        season_from_file = re.findall(REGEX_SEASON_NR,cleaned_path[1])
        if not season_from_file:
            return "1"
        else:
            return season_from_file[0]
    else:
        return season_from_dir[0]

def scrape_name(cleaned_path):
    name = re.findall(REGEX_NAME,cleaned_path[0])
    if not name:
        return "NULL"
    else:
        return name[0]
