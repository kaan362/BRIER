import { supabase } from '../../lib/supabase'
import Link from 'next/link'

export default async function Leaderboard() {
  const { data: analysts } = await supabase
    .from('analysts')
    .select('*')
    .order('win_rate', { ascending: false })

  return (
    <main className="max-w-2xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">Brier Leaderboard</h1>
      <table className="w-full border-collapse">
        <thead>
          <tr className="border-b text-left text-sm font-semibold text-red-700">
            <th className="p-2">Analist</th>
            <th className="p-2">Win Rate</th>
            <th className="p-2">Tahmin Sayısı</th>
          </tr>
        </thead>
        <tbody>
          {analysts?.map((analyst) => (
            <tr key={analyst.id} className="border-b">
              <td className="p-2">
                <Link href={`/analyst/${analyst.id}`} className="text-indigo-600 hover:underline">
                  {analyst.display_name}
                </Link>
              </td>
              <td className="p-2">{analyst.win_rate !== null ? `${analyst.win_rate.toFixed(1)}%` : "no data"}</td>
              <td className="p-2">{analyst.sample_size ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}