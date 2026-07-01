import { supabase } from '../../lib/supabase'

export default async function Leaderboard() {
  const { data: analysts } = await supabase
    .from('analysts')
    .select('*')
    .order('win_rate', { ascending: false })

  return (
    <main>
      <h1>Brier Leaderboard</h1>
      <table>
        <thead>
          <tr>
            <th>Analist</th>
            <th>Win Rate</th>
            <th>Tahmin Sayısı</th>
          </tr>
        </thead>
        <tbody>
          {analysts?.map((analyst) => (
            <tr key={analyst.id}>
              <td>{analyst.display_name}</td>
              <td>{analyst.win_rate !== null ? `${analyst.win_rate.toFixed(1)}%`:"no data"}</td>
              <td>{analyst.sample_size ?? "-"}</td>
            </tr>
        
          ))}
        </tbody>
      </table>
    </main>
  );
}