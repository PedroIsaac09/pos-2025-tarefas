let offset = 0;
const limit = 12;
const API_URL = "https://pokeapi.co/api/v2/pokemon";

const pokemonList = document.getElementById("pokemonList");
const pokemonDetails = document.getElementById("pokemonDetails");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");
const splash = document.getElementById("splash");
const pokeball = document.getElementById("pokeball");

// Exibir detalhes
async function carregarDetalhes(urlOrName) {
  try {
    const response = await fetch(
      urlOrName.startsWith("http") ? urlOrName : `${API_URL}/${urlOrName.toLowerCase()}`
    );
    if (!response.ok) throw new Error("Pokémon não encontrado");

    const pokemon = await response.json();

    pokemonDetails.innerHTML = `
      <div class="d-flex flex-column align-items-center">
        <img src="${pokemon.sprites.other['official-artwork'].front_default}" 
             alt="${pokemon.name}" 
             class="pokemon-img mb-3">
        <h3 class="text-capitalize fw-bold">${pokemon.name}</h3>
        <span class="badge bg-dark fs-6 mb-3">#${pokemon.id}</span>
      </div>
      <hr>
      <p><strong>Altura:</strong> ${pokemon.height / 10} m</p>
      <p><strong>Peso:</strong> ${pokemon.weight / 10} kg</p>
      <p><strong>Habilidades:</strong></p>
      ${pokemon.abilities.map(ab => `<span class="badge bg-primary ability-badge">${ab.ability.name}</span>`).join("")}
      <hr>
      <p><strong>Tipos:</strong></p>
      ${pokemon.types.map(tp => `<span class="type-badge type-${tp.type.name}">${tp.type.name}</span>`).join("")}
    `;
  } catch (error) {
    pokemonDetails.innerHTML = `<div class="alert alert-danger">❌ Pokémon não encontrado</div>`;
  }
}

// Carregar lista
async function carregarPokemons() {
  try {
    const response = await fetch(`${API_URL}?offset=${offset}&limit=${limit}`);
    const data = await response.json();

    pokemonList.innerHTML = "";
    data.results.forEach(pokemon => {
      const li = document.createElement("li");
      li.className = "list-group-item text-capitalize d-flex justify-content-between align-items-center";
      li.textContent = pokemon.name;

      const span = document.createElement("span");
      span.innerHTML = "🔍";
      li.appendChild(span);

      li.addEventListener("click", () => carregarDetalhes(pokemon.url));

      pokemonList.appendChild(li);
    });
  } catch (error) {
    pokemonList.innerHTML = `<li class="list-group-item text-danger">Erro ao carregar Pokémons</li>`;
  }
}

// Paginação
prevBtn.addEventListener("click", () => {
  if (offset >= limit) {
    offset -= limit;
    carregarPokemons();
  }
});
nextBtn.addEventListener("click", () => {
  offset += limit;
  carregarPokemons();
});

// Pesquisa
searchForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const query = searchInput.value.trim();
  if (query) {
    carregarDetalhes(query);
    searchInput.value = "";
  }
});

// Splash interativo
pokeball.addEventListener("click", () => {
  splash.style.display = "none";
  carregarPokemons();
});
