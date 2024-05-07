import json

#read dataset
with open('originalgamesdata.json', 'r') as file:
    existing_data = json.load(file)

#initialize an empty list for storing games
games = []
# Set a counter to limit the number of intents processed
counter = 0

#iterate over each item in the dataset
for item in existing_data:
    #increment the counter
    counter += 1

    #extract relevant information
    name = item.get("name", "not available")
    popu_tags = item.get("popu_tags", []) #genres
    categories = item.get("categories", []) #genres
    full_desc = item.get("full_desc", {}).get("desc", "not available")
    release_date = item.get("date", "not available")
    developer = item.get("developer", "not available")

    #ensure popu_tags, price, and categories are lists
    popu_tags = [popu_tags] if isinstance(popu_tags, str) else popu_tags
    categories = [categories] if isinstance(categories, str) else categories
    release_date = [release_date]
    developer = [developer]

    #limit patterns to 6 relevant ones
    patterns = popu_tags[:2] + categories[:2] + release_date + developer

    #convert full_desc to string if it's a dictionary
    full_desc = full_desc if isinstance(full_desc, str) else str(full_desc)

    #remove "About This Game" prefix if present in description
    full_desc = full_desc.replace("About This Game", "").strip()

    #shorten the full_desc to a summary of 3-5 sentences
    summary_sentences = full_desc.split(". ")[:5]
    shortened_desc = ". ".join(summary_sentences)

    #create game intent
    new_game = {
        "tag": name,
        "patterns": patterns,
        "responses": [shortened_desc],
        "release_date": release_date,
        "developer": developer,
        "context_set": ""
    }

    # add the new game intent to the list
    games.append(new_game)

    # counter checks if it has reached the limit
    if counter >= 20000:
        break

#create new JSON data structure
new_data = {"games": games}

#write the new JSON data to a file
with open('games.json', 'w') as file:
    json.dump(new_data, file, indent=4)