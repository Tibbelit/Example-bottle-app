# Vi importerar de funktioner som vi behöver från bottle
from bottle import run, route, template, static_file, request, redirect

def read_movies_from_file():
	'''
	Läser in våra filmer från textfilen och returnerar de som en lista
	
	Returns:
		list
	'''
	movies = []
	try:
		# Öppnar filen "movies.txt"
		my_file = open("storage/movies.txt", "r")
		# Läser in filens innehåll
		content = my_file.read()
		# För varje rad i filen (alltså för varje filmtitel)
		for movie in content.split("\n"):
			# Kontrollerar så att filmtiteln ej är tom (en rom rad i filen)
			if movie != "":
				# Lägger till filmtiteln i vår lista över filmtitlar
				movies.append(movie)
		# Returnerar filmtitlarna i en lista
		return movies
	except:
		# Om filen "movies.txt" inte finns, så skapar vi den
		my_file = open("storage/movies.txt", "w").close()
		return movies

# Routen "/" innebär adressen "http://127.0.0.1:8000/"
@route("/")
def index():
	'''
		Visar upp vår startsida, men filmerna som finns lagrade
	'''
	# Läser in filmtitlarna från vår text-fil
	movies_from_file = read_movies_from_file()
	# Returnerar mallen "index" (som finns i mappen "views/index.html")
	# Vi skickar än med filmerna som ska skrivas ut men nyckeln "movies"
	return template("index", movies=movies_from_file)

# Routen "/add-movie" innebär adressen "http://127.0.0.1:8000/add-movie"
# method="POST" innebär att man bara tillåter http-anrop av typen "POST"
@route("/add-movie", method="POST")
def save_movie():
	'''
		Sparar en filmtitel som skickats från formuläret
		i vår textfil "movies.txt"
	'''
	# Hämtar titeln som skickats från formuläret (med name="title")
	title = request.forms.get("title")
	# Öppnar vår fil i "lägg till"-läge
	my_file = open("storage/movies.txt", "a")
	# Skriver filmtiteln med en radbrytning sist i filen
	my_file.write(title + "\n")
	# Stänger filen
	my_file.close()
	# Skickar användaren till routen "/"
	redirect("/")

# En route som hanterar våra statiska filer (css/bilder/js/etc.)
@route("/static/<file_name>")
def static_files(file_name):
	'''
		Returnerar statiska filer från mappen "static"
		
		Args:
			file_name(str) : Namnet på filen vi vill returnera
	'''
	# Returnerar den efterfrågade filen
	return static_file(file_name, root="static")

# Startar vår webbserver, med addressen: 127.0.0.1:8000
run(host="127.0.0.1", port="8000")