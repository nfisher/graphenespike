HTML = '''<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/graphiql/0.11.11/graphiql.min.css" integrity="sha256-gSgd+on4bTXigueyd/NSRNAy4cBY42RAVNaXnQDjOW8=" crossorigin="anonymous" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fetch/1.1.1/fetch.min.js" integrity="sha256-TQsP3yTWwfvm6Auy90oBeVhYhGZuKa1jRM3vpnQpX+8=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/15.6.2/react.min.js" integrity="sha256-c/17te7UpABi7+wcIHAAiIMOrNMVcTIzoxtRTDoYB4s=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/15.6.2/react-dom.min.js" integrity="sha256-Xhtg7QJuNhwB5AzaUcgr0iqNtCitzN+c/6k5/SOtENU=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/graphiql/0.11.11/graphiql.min.js" integrity="sha256-oeWyQyKKUurcnbFRsfeSgrdOpXXiRYopnPjTVZ+6UmI=" crossorigin="anonymous"></script>
    <title>GraphiQL</title>
  </head>
  <body style="width: 100%; height: 100%; margin: 0; overflow: hidden;">
    <div id="graphiql" style="height: 100vh;">Loading...</div>
    <script>
      "use strict";
      var headers = new Headers();
      headers.set("Content-Type", "application/json");

      function graphQLFetcher(graphQLParams) {
        return fetch("graphql?raw", {
          method: "post",
          headers: headers,
          body: JSON.stringify(graphQLParams),
        }).then(function (response) {
          return response.text();
        }).then(function (responseBody) {
          try {
            return JSON.parse(responseBody);
          } catch (error) {
            return responseBody;
          }
        });
      }

      ReactDOM.render(
        React.createElement(GraphiQL, {fetcher: graphQLFetcher}),
        document.getElementById("graphiql")
      );
    </script>
  </body>
</html>'''