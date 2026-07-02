import Link from 'next/link'

export default function Home() {
  return (
    <main className="max-w-2xl mx-auto p-8">
      <h1 className="text-6xl font-bold mb-4">Brier</h1>
      <p className="text-gray-600 mb-6">
        WELCOME TO BRIER, A PLATFORM FOR TRACKING AND ANALYZING PREDICTIONS MADE BY ANALYSTS. EXPLORE THE LEADERBOARD TO SEE TOP PERFORMERS OR VIEW INDIVIDUAL ANALYSTS TO ASSESS THEIR PREDICTION HISTORY AND PERFORMANCE.
      </p>
      <Link
        href="/leaderboard"
        className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Leaderboard'a Git →
      </Link>
    </main>
  );
}