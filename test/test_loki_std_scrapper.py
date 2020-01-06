from atlas.scrapper_plugins.loki_std_scrapper import clean_path,scrape_episode_nr,scrape_season_nr,scrape_name

def test_clean_path():
    shallow = "movie.mkv"
    one_deep = "alpha/movie.mkv"
    two_deep = "beta/alpha/movie.mkv"
    assert clean_path(shallow)  == ("","movie")
    assert clean_path(one_deep) == ("alpha","movie")
    assert clean_path(two_deep) == ("alpha","movie")

    dirty_shallow = "(1080p)[dingus]movie(spam).mkv"
    dirty_one_deep = "[alpha]alpha(or)/(1080p)[dingus]movie(spam).mkv"
    dirty_two_deep = "[alpha]alpha(or)/(1080p)[dingus]movie(spam).mkv"

    assert clean_path(dirty_shallow)  == ("","movie")
    assert clean_path(dirty_one_deep) == ("alpha","movie")
    assert clean_path(dirty_two_deep) == ("alpha","movie")

    spaced_shallow = "(1080p)[dingus]movie.a(spam).mkv"
    spaced_one_deep = "[alpha]alpha(or).king/(1080p)[dingus]movie_b(spam).mkv"
    spaced_two_deep = "/car/[alpha]alpha_centry(or)/(1080p)[dingus]movie_c(spam).mkv"

    assert clean_path(spaced_shallow)  == ("","movie a")
    assert clean_path(spaced_one_deep) == ("alpha king","movie b")
    assert clean_path(spaced_two_deep) == ("alpha centry","movie c")



def test_scrap_episode_nr():
    alpha  = clean_path("/car/[alpha]alpha_sentry(or)/(1080p)[dingus]alpha_sentry.episode4(spam).mkv")
    beta   = clean_path("/car/[alpha]Live.La.Live(or)/(1080p)[dingus]Live.La.Live.s1.e2(spam).mkv")
    charlie = clean_path("./Sandwich Card/Sandwich Card - 1x20 - Makeshift.mkv")
    delta = clean_path("./[DingoCar] Sweet 323 - Alice [1080p]/[DingoCar] Sweet 323 - Alice - 13 [1080p].mkv")
    echo = clean_path("./[SAbanat] Djingo - Deathscarse Egypt Arc [1080p]/[SAbanat] Djingo - Deathscarse Egypt Arc - 46 [1080p].mkv")
    ova    = clean_path("/dingus/(1080p)LaserDwisk[red]/LaserDwisk.ova.mkv")

    assert scrape_episode_nr(alpha) == "4"
    assert scrape_episode_nr(beta) == "2"
    assert scrape_episode_nr(charlie) == "20"
    assert scrape_episode_nr(delta) == "13"
    assert scrape_episode_nr(echo) == "46"
    assert scrape_episode_nr(ova) == "0"

def test_scrap_season_nr():
    alpha = clean_path("/ding/[alad].The.Rim.Sons.Season.3.1080p/S3E1.mkv")
    beta  = clean_path("/Firefod/Red.Morning.S4/Red.Morning.episode.3.mkv")
    charlie = clean_path("/DeadorDead(2019)/episode4.mkv")

    assert scrape_season_nr(alpha)  == "3"
    assert scrape_season_nr(beta)   == "4"
    assert scrape_season_nr(charlie) == "1"

def test_scrape_name():
    alpha = clean_path("./Dr Noodles [H.265]/Dr.Noodles.S2/[SAsa]Dr_Noodles_-_045_(Triple Audio_10bit_BD1080p_x265).mkv")
    beta = clean_path("./Full.plastic.car.S01.720p.BluRay.FLAC2.0.x264-NTb/Full.plastic.car.S01E38.Conflict.in.Toilet.720p.BluRay.FLAC2.0.x264-NTb.mkv")
    charlie = clean_path("./Family.snowboarding.adventure.2012.S02.1080p.WEBRip.x264-SpaceFart/[SpaceFart] Family snowboarding adventure - Alpine Rush - 05 [1080p].mkv")

    assert scrape_name(alpha)  == "Dr Noodles"
    assert scrape_name(beta)   == "Full plastic car"
    assert scrape_name(charlie) == "Family snowboarding adventure 2012"