from bs4 import BeautifulSoup
import requests
import sqlite3

def fix_name_data(name_data):
    name_data = str(name_data).split(">")
    name_data = name_data[1].split("\n")
    name_data = name_data[0]
    return name_data

def fix_homeworldAndGender_data(home):
    home = str(home).split(">")
    home = home[1].split("<")
    home = home[0]
    return home

def fix_affiliations_data(aff):
    res_list = []
    for af in aff:
        af = str(af).split(">")
        af = af[2].split("<")
        af = af[0]
        res_list.append(af)
    return res_list  

def fix_species_data(species):
    species = str(species).split("/")
    species = species[1].split('"')
    return species[0]

def haloSearch(listy):

    conn = sqlite3.connect("HaloData.db")
    c = conn.cursor()
    
    for index,el in enumerate(listy):
        try:
            
            URL= f"https://www.halopedia.org/{el}"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            

            # Scraping elements on the page to find what we need and saving to vars
            results = soup.find("table",{"class":"infobox"})
            homeworld_search = results.find_all("a")
            affiliation_search = results.find_all("li")
            gender_search = results.find_all("p")

            # Narrowing down info from those vars set above
            name = results.find("th")
            homeworld = homeworld_search[1]
            affiliations = affiliation_search[:2]
            gender = gender_search[7]
            species = gender_search[5]
            
            # I would like to have partial data in the db, if possible, so try/excepts are handling partial data loss
            try:
                #nd = str(fix_name_data(name))
                nd = el
            except:
                nd = el
                
            try:
                sd = str(fix_species_data(species))
            except:
                sd = "N/A"
                
            try:
                hd = str(fix_homeworldAndGender_data(homeworld))
            except:
                hd = "N/A"
                
            try:
                gd = str(fix_homeworldAndGender_data(gender))
            except:
                gd = "N/A"
                
            try:
                ad = str(fix_affiliations_data(affiliations)[0] + ", " + fix_affiliations_data(affiliations)[1])
            except:
                ad = "N/A"
                

            print(f"Done with {index}/{len(listy)}: {el}")

            c.execute("INSERT INTO halo VALUES(?,?,?,?,?)",(nd,sd,hd,gd,ad))
            conn.commit()
            
        except:
            print(f"Skipping {index}/{len(listy)}: {el}")

    c.close()
        
        

halo_names = [
    'Akato_%27Dakaj',
    'Ang%27napnap_the_Enlightened',
    'Arbiter_(Killer_Instinct)',
    'Aristocrat',
    'Asum_%27Mdama',
    'Ava_Lang',
    'Avery_Johnson',
    'Awlphhum_Who_Became_Tolerable',
    'Bal%27Tol_%27Xellus',
    'Breaking_Shadow',
    'Dinnat_%27Hilot',
    'Dural_%27Mdama',
    'Edward_Buck',
    'Edward_Davis',
    'Ethan_Graves',
    'Fal_%27Chavamee',
    'Fireteam_Crimson',
    'Forze_%27Mdama',
    'Frederic-104',
    'Gerdon_%27Hilot',
    'Gray_Maiden_of_Konar',
    'Gray_Maiden_of_Konar',
    'Holly_Tanaka',
    'Jameson_Locke',
    'John-117',
    'Jora_%27Konaree',
    'Judge-King_of_Qivro',
    'Jul_%27Mdama',
    'Juran',
    'Kasha_%27Hilot',
    'Kel_%27Darsam',
    'Kelly-087',
    'Koida_%27Vadam',
    'Kojo_Agu',
    'Krith',
    'Lak_%27Vadamee',
    'Levu_%27Mdama',
    'Linda-058',
    'Marcus_Hudson',
    'Michael_Crespo',
    'Mken_%27Scre%27ah%27ben',
    'Mken_%27Scre%27ah%27ben',
    'Murok_%27Vadam',
    'Mvon_%27Sraom',
    'N%27tho_%27Sraom',
    'N%27tho_%27Sraom',
    'N%27Zursa_%27Xellus',
    'Naxan_%27Mdama',
    'Nesh_%27Radoon',
    'Nicole-458',
    'Olympia_Vale',
    'Ori_%27Sumai',
    'Orok_%27Darsam',
    'Ossis_%27Xellus',
    'Panom',
    'Pelahsar_the_Strident',
    'Qurlom',
    'Raia_%27Mdama',
    'Ripa_%27Moramee',
    'Rojka_%27Kasaan',
    'Rookie',
    'Rukt',
    'Sarah_Palmer',
    'Skimmer_Alpha',
    'Soha_%27Rolamee',
    'Sooln_%27Xellus',
    'SPARTAN-B312',
    'Taylor_Miles',
    'Terrence_Hood',
    'Thel_%27Vadam',
    'Thel_%27Vadam',
    'Ther_%27Vadam',
    'Tobias_Fleming_Shaw',
    'Toha_%27Sumai',
    'Tul_%27Juran',
    'Tulum_%27Juranai',
    'Unidentified_Spartan-IV',
    'Ussa_%27Xellus',
    'Ussa_%27Xellus',
    'Usze_%27Taham',
    'Veronica_Dare',
    'Victor_Ramos',
    'Wallace_Fujikawa',
    'Yayep_the_Archdeacon_of_Indolence',
    "12-9F5",
    "434_Combat_Readiness_Lab",
    "957-A3",
    "957-A4",
    "Acoustic_dampening_field",
    "Age_of_Abandonment",
    "Ages_of_Conflict",
    "Ages_of_Conversion",
    "Ages_of_Discovery",
    "Ages_of_Doubt",
    "Ages_of_Reclamation",
    "Ages_of_Reconciliation",
    "AirCare_Ambulance",
    "Aleutian_Rim",
    "Ancient_humanity",
    "Armored_Warthog",
    "Ascension_(ceremony)",
    "Asceticism",
    "Ascon",
    "AV-30_Kestrel",
    "B'ashamanune",
    "Bacigalupi_Memorial_Nature_Preserve",
    "Bandusa_Insurrectionist_group",
    "Banished",
    "Beholders_of_the_One_Vapor",
    "Biko_Independence_Army",
    "Bison",
    "Black_Reef",
    "Blaze_of_Glory",
    "Bloodbrave_Guardian_of_Suban",
    "Blue_Mandibles",
    "Bondi_Beach",
    "Boson_Research_Facility",
    "Bronto",
    "Bulwark_of_Bone",
    "Cargo_walker",
    "Castra",
    "Castra_Arcology",
    "Chalybs_Testing_Preserve",
    "Chancellor's_Guards",
    "Charum_Hakkor_arena",
    "Chelsea_Trauma_Center",
    "Citadel_Charum",
    "Civet",
    "Clan_of_the_Long_Shields",
    "Clan_of_the_Ravaged_Tusks",
    "Colonial_Administration_Authority",
    "Colony's_swarm",
    "Conduction_Refinement_Facility",
    "Covenant",
    "Covenant",
    "Covenant_Battle_Calendar",
    "Covenant_fringe",
    "Covenant_laws",
    "Covenant_loyalists",
    "Covenant_military",
    "Covenant_religion",
    "Covenant_remnants",
    "Covenant_remnants",
    "Covenant_separatists",
    "Covenant_separatists",
    "Cowling",
    "Created",
    "Crystal",
    "Cupid's_Knife",
    "Currahee_Special_Assembly_Plant_2",
    "Denisovan",
    "Dipholekgolo",
    "Doozy",
    "Ecumene",
    "EM-240_Neides_auger",
    "EM-240_Neides_auger",
    "Epsilon_Expanse",
    "Erde-Tyrene_civilization",
    "Eridanus_Government",
    "Fibril_cutter",
    "Fire_and_Repentance_Codices",
    "Fireball_Warthog",
    "Flame_Warthog",
    "Flats_of_Forever",
    "FLEETCOM_Sector_Three/Subvolume_D-6",
    "Flood",
    "Flood",
    "Florian",
    "Forerunner",
    "Forklift",
    "Forseti_Northern_Terminus_37",
    "Fougasse",
    "Free-fire_area_OZONE",
    "Freedom_and_Liberation_Party",
    "Frieden",
    "Galodew_Emancipation",
    "Gao_Liberation_Force",
    "Gao_Republic",
    "Gasgira",
    "Gekz",
    "Giant's_Armory",
    "Glassing",
    "Governors_of_Contrition",
    "Hall_of_Eternity",
    "Haven_arcology",
    "Heart_of_Tala",
    "High_Council",
    "Highway_(Charum_Hakkor)",
    "History_of_the_Covenant",
    "HJ3-213",
    "Homestead_Facility",
    "Human",
    "Human_weaponry",
    "Human-San'Shyuum_alliance",
    "Huragok",
    "Hyperion_Station",
    "Io_Design_Lab",
    "IX-KA_anomaly",
    "Jazz-9",
    "Jiralhanae",
    "John_Forge's_Warthog",
    "JOTUN_Arilus",
    "JOTUN_Arilus",
    "Joyous_Exultation_Covenant",
    "Jul_'Mdama's_Covenant",
    "K'tamanune",
    "Kaepra's_Grief",
    "Keepers_of_the_One_Freedom",
    "Kelvin_Research_Station",
    "Kerrec_Irruption",
    "Khantolekgolo",
    "Kig-Yar",
    "Komodo",
    "Komodo",
    "Koslovics",
    "Lacerta_erectus",
    "Laser",
    "Legion_of_the_Corpse-Moon",
    "Lekgolo",
    "Lemuria_(province)",
    "Liang-Dortmund_mining_rig",
    "List_of_unidentified_species",
    "Long_Range_Stealth_Orbital_Insertion_Pod",
    "Low/Zero_Gravity_Testing_Facility",
    "Luna_Confederated_States",
    "Lydus'_clan",
    "M-100627",
    "M12_Chaingun_Warthog",
    "M12_Warthog",
    "M121_Jackrabbit",
    "M12A1_Rocket_Warthog",
    "M12B_Warthog",
    "M12G1_Gauss_Warthog",
    "M12R_Rocket_Warthog",
    "M12S_Warthog_CST",
    "M145D_Rhino",
    "M15_Razorback",
    "M274_Mongoose",
    "M274R_Mongoose",
    "M290_Mongoose",
    "M312_Elephant",
    "M313_Elephant",
    "M318_Elephant",
    "M400_Kodiak",
    "M510_Mammoth",
    "M552_Sandcat",
    "M650_Mastodon",
    "M808_Scorpion",
    "M808B2_Sun_Devil",
    "M808B3_Tarantula",
    "M831_Troop_Transport_Warthog",
    "M850_Grizzly",
    "M862_Arctic_Warthog",
    "M864_Arctic_Warthog",
    "M868_Tropic_Warthog",
    "M9_Wolverine",
    "M914_Recovery_Vehicle",
    "Maglev_train",
    "Mark_of_Disobedience",
    "Mark_of_Shame",
    "Mato_Grosso",
    "Merg_Vol's_Covenant",
    "Mgalekgolo",
    "Mind_transfer",
    "Ministry",
    "Ministry_of_Infidels",
    "Ministry_of_Inquisition",
    "Mongoose_(fiction)",
    "Munitions_loader",
    "Murat_gun_truck",
    "Nanotechnology",
    "Narcozine_gas",
    "Neo-Friedenism",
    "New_Atlantic_Province",
    "New_Barbados",
    "New_Colonial_Alliance",
    "Nornfang",
    "Oathsworn",
    "Overwatch_Construction_Platform",
    "Paint_pellet_gun",
    "Palaikos_borderlands",
    "Path_Kethona_Forerunner",
    "Path_Kural",
    "Path_of_Control",
    "People's_Occupation",
    "People's_Occupation_Government",
    "Powder_wagon",
    "Powered_exoskeleton",
    "Prayer_for_the_Fallen",
    "Precursor",
    "Precursor",
    "Progression_of_the_Ages",
    "Project_HOGSTICKER",
    "Pugil_stick",
    "Quad_walker",
    "Rally_Point_Zulu",
    "Ratification_Parley",
    "Red_Slate_Plateau",
    "Red_Team's_Warthog",
    "Reformists",
    "Reliquary",
    "Rescue_crawler",
    "Revolution",
    "Rhulolekgolo",
    "Roamer",
    "Rocket-propelled_grenade",
    "Rolls_of_honor",
    "Sali_'Nyon's_Covenant",
    "San'Shyuum",
    "San'Shyuum_flotilla",
    "Sanderson_Private_Hospital",
    "Sangheili",
    "Sclera_of_Chu'ot",
    "Scooter",
    "Scout_Warthog",
    "Scyllion_Warehouse_District",
    "Secessionist_Union",
    "Señora_Sies",
    "Servants_of_the_Abiding_Truth",
    "Sesa_'Refumee's_heretic_faction",
    "Sesa_'Refumee's_heretic_faction",
    "Shields_of_Requiem",
    "Siege_bike",
    "Simulated_Warthog_variant",
    "Single_Occupant_Exoatmospheric_Insertion_Vehicle",
    "Site_Yankee-002-G3",
    "Skyfire_Exosuit",
    "SP42_Cobra",
    "Spartan_1.1_faction",
    "Sperry_FCMMagLEV",
    "Stealth_Kodiak",
    "Stoics",
    "Stormbreak",
    "Struggle_for_Ideological_Purity",
    "Stylus",
    "Sword_Warthog",
    "Swords_of_Sanghelios",
    "T'vaoan",
    "Target_Area_Apache",
    "TB-SB-1",
    "Technological_Achievement_Tiers",
    "Tem'Bhetek's_faction",
    "Terraforming",
    "Thanolekgolo",
    "The_Fort",
    "Thieves_of_the_Claw",
    "Tram",
    "Transit_Node_Bhadra",
    "Translation_disk",
    "Trooper_Warthog",
    "True_Sayings",
    "Tudejsa",
    "Tundra_Warthog",
    "Tunnel_Weasel",
    "Typhoon",
    "UE8-14",
    "Unggoy",
    "Unggoy_government",
    "Unidentified_automatic_pistol",
    "Unidentified_insurrectionist_group",
    "Unified_Earth_Government",
    "United_Nations",
    "United_Nations_Space_Command",
    "United_Rebel_Front",
    "UNSC_escape_pod",
    "UNSC_starship",
    "UNSC_Symphony_Hall",
    "Urban_Warthog",
    "User:Cally99117/Drafts/4",
    "Ussans",
    "Valorguards_of_the_Chosen",
    "Vanguard_Kodiak",
    "Vanguard_Wolverine",
    "Vata_'Gajat's_mercenary_group",
    "Venezian_Militia",
    "Vespin_Warthog",
    "Vestol_Simulation_Lab",
    "Veteran_Jackrabbit",
    "Veteran_Mantis",
    "Vhalkem",
    "VTOL",
    "VX_7_nerve_gas",
    "War_of_Beginnings",
    "Warriors_of_Malaston",
    "Warthog",
    "Whispered_Truth",
    "Wild_Jackrabbit",
    "Woodland_Warthog",
    "Writ_of_Union",
    "X-24_FAV",
    "Xalanyn",
    "XRP12_Gremlin",
    "Yanme'e",
    "Yonhet",
]



haloSearch(halo_names)