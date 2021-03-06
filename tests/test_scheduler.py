import PullRequest
import unittest
from mock import patch, MagicMock

class SchedulerTestCase(unittest.TestCase):

    @patch('PullRequest.logging')
    @patch('PullRequest.fetch_reviews')
    @patch('PullRequest.github')
    def test_get_pull(self, github, fetch_reviews, logging):
        user = MagicMock()
        user.login = 'login'
        user.date = 5
        pull = MagicMock()
        pull.title = 'title'
        pull.user = user
        pull.commits = 4

        commit = MagicMock()
        commit.author = user

        commits = MagicMock()
        commits.reversed = [commit]

        pull.get_commits.return_value = commits

        contributor = MagicMock()
        contributor.total = 10
        contributor.author = user

        repo = MagicMock()
        repo.get_stats_contributors.return_value = [
            contributor
        ]

        github_object = MagicMock()
        github.Github.return_value = github_object
        pulls = [
            pull
        ]

        github_object.get_repo.return_value = repo
        repo.get_pulls.return_value = pulls

        def fetch_reviews_mock(token):
            print('fetch_reviews')
        fetch_reviews = fetch_reviews_mock

        PullRequest.check_pull_requests()

        self.assertEqual(logging.info.call_args, (('Would merge now',),))


if __name__ == '__main__':
    unittest.main()
