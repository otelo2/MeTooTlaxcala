const search = document.getElementById('search');
const matchList = document.getElementById('match-list');

//Searchs for the abusers in the abusador.json and filters them
const searchAbusers = async searchText => {
    const res = await fetch('../Frontend/data/abusador.json');
    const abusers = await res.json();

    //Get matches to current text input
    let matches = abusers.filter(abuser => {
        const regex = new RegExp(`^${searchText}`, 'gi');
        return abuser.nombre.match(regex) || abuser.apellidopaterno.match(regex) || abuser.apellidomaterno.match(regex);
    });

    if(searchText.length === 0) {
        matches = [];
        matchList.innerHTML = ''
    }

    outputHtml(matches);
}

//Show results in HTML
const outputHtml = matches => {
    if(matches.length > 0) {
        const html = matches.map(match => `
            <div class="card card-body mb-1">
                <h4>${match.nombre} ${match.apellidopaterno} ${match.apellidomaterno} <span class="text-primary">${match.nombre}</span></h4>
                <small>Lat: ${match.fecha} / Long: ${match.hora}</small>
            </div>
        `
        ).join('');

        matchList.innerHTML = html;
    }
}

search.addEventListener('input', () => searchAbusers(search.value));