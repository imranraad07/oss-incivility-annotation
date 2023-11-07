# GitHub-locked-issues
Data collection from GitHub

Criteria for our data collection for issue threads:
* Number of collaborators inside the project > 99
* At least one issue thread locked with **'too-heated'** as the reason
* At least a total of 500 issue threads inside the project

Our data is a combination of the following sources:
* GitHub API
* Google Cloud GitHub Archive

Data collected up until now:
**234** heated-locked issues from **126 projects**

Google Cloud Query:
```
SELECT
 repo,
 login,
 year,
 url,
 title,
 reason,
 comment_count,
 num_issues,
 num_stars
FROM (
 SELECT
   repo.name AS repo,
   actor.login AS login,
   JSON_EXTRACT(payload,
     '$.issue.created_at') AS year,
   JSON_EXTRACT(payload,
     '$.issue.html_url') AS url,
   JSON_EXTRACT(payload,
     '$.issue.active_lock_reason') AS reason,
   JSON_EXTRACT(payload,
     '$.issue.title') AS title,
   JSON_EXTRACT(payload, '$.issue.comments') AS comment_count
 FROM
   `githubarchive.year.2022`
 WHERE
   type = 'IssuesEvent'
) AS issues_data
LEFT JOIN (
 SELECT
   repo.name AS repo_name,
   COUNT(*) AS num_issues
 FROM
   `githubarchive.year.2022`
 WHERE
   type = 'IssuesEvent'
 GROUP BY
   repo_name
 HAVING COUNT(*) > 1
) AS num_issues_data
ON issues_data.repo = num_issues_data.repo_name
LEFT JOIN (
 SELECT
   repo.name AS repo_name,
   COUNT(*) AS num_stars
 FROM
   `githubarchive.year.2022`
 WHERE
   type = 'WatchEvent'
 GROUP BY
   repo_name
 HAVING COUNT(*) > 1
) AS num_stars_data
ON issues_data.repo = num_stars_data.repo_name
WHERE
 reason LIKE '%too heated%'
 AND CAST((comment_count) AS INT64) >= 4
LIMIT
 5000;
```
