function AllChannels() {
    
    const [channels, setChannels] = React.useState([])

    React.useEffect(() => {
        fetch('/api/search')
        .then((response) => response.json())
        .then((data) => setMovies(data.movies))
      }, [])
    
    const movieList = []

    for (const movie of movies) {
        movieList.push(
            <div>
                <p>Title: {movie.title}</p>
                <p>Overview: {movie.overview}</p>
                <p>Release Date: {movie.release_date}</p>
                <p>Poster Path: {movie.poster_path}</p>
            </div>
        )
    }
    
    return(
        <div>{movieList}</div>
    );
}

ReactDOM.render(
    <AllMovies />,
    document.querySelector('#root')
)