// Minimal app.js to wire habits and P&L
document.addEventListener('DOMContentLoaded', ()=>{
  const habitsEl = document.getElementById('habits')
  fetch('data/habits.json').then(r=>r.json()).then(d=>{
    d.habits.forEach(h=>{
      const li = document.createElement('div')
      li.innerHTML = `<strong>${h.title}</strong> — ${h.category} — score: ${(h.score*100).toFixed(0)}% — streak: ${h.streak}`
      habitsEl.appendChild(li)
    })
  })
})

function calculatePnLByR(rMul, riskPct, account){
  const pnlPct = rMul * riskPct
  return {pnlPct: pnlPct, pnlUsd: account * (pnlPct/100)}
}

window.calculatePnLByR = calculatePnLByR
