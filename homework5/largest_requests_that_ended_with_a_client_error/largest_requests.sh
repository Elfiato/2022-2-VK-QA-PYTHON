echo Largest requests that ended with a client error > largest_requests_that_ended_with_a_client_error.txt; awk '{base_url = "http://almhuette-raith.at/"; if ($7 ~ base_url".*") url = substr($7, length(var)); else url = $7; if ($9 ~ /4../) print($10, url, $9, $1)}' ../access.log | sort -nr | head -n 5 | awk '{printf("%s\n%s\n%s\n%s\n", $2, $3, $1, $4)}' >> largest_requests_that_ended_with_a_client_error.txt