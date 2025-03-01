from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = None

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	recipeName = recipeName.replace('-', ' ').replace('_', ' ')
	recipeName = re.sub(r'[^a-zA-Z\s]', '', recipeName)

	words = [word.capitalize() for word in recipeName.split() if word]
	return ' '.join(words)


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	data = request.get_json()

	if data.get('name') in cookbook:
		return '', 400

	match data.get('type'):
		case 'recipe':
			if data.get('cookTime', -1) < 0:
				return '', 400

			cookbook[data.get('name')] = Ingredient(
				name=data.get('name'),
				cook_time=data.get('cookTime')
			)
		case 'ingredient':
			item_names = set()
			for item in data.get('requiredItems', []):
				if item.get('name') in item_names:
					return '', 400
				item_names.add(item.get('name'))

			cookbook[data.get('name')] = Recipe(
				name=data.get('name'),
				required_items=[
					RequiredItem(
						name=item.get('name'),
						quantity=item.get('quantity')
					) 
					for item in data.get('requiredItems', [])
				]
			)
		case _:
			return '', 400


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
