/* Phase 3: next action from the existing Phase 1 checklist. */
(()=>{"use strict";
const tasks=[
 {id:"id",ar:"تفعيل DigiD",nl:"DigiD activeren",url:"./articles/digid-registration-guide.html",source:"https://www.digid.nl/"},
 {id:"insurance",ar:"التحقق من التأمين الصحي",nl:"Zorgverzekering controleren",url:"https://www.rijksoverheid.nl/onderwerpen/zorgverzekering",source:"https://www.rijksoverheid.nl/onderwerpen/zorgverzekering"},
 {id:"tax",ar:"مراجعة الضرائب",nl:"Belastingen controleren",url:"./articles/annual-tax-return-2026.html",source:"https://www.belastingdienst.nl/"},
 {id:"study",ar:"اختيار الدراسة ومراجعة DUO",nl:"Studie kiezen en DUO controleren",url:"./articles/mbo-conditions.html",source:"https://www.duo.nl/"},
 {id:"work",ar:"مراجعة عقد العمل",nl:"Arbeidscontract controleren",url:"./articles/employment-contracts-labor-law-2026.html",source:"https://www.rijksoverheid.nl/onderwerpen/arbeidsovereenkomst-en-cao"},
 {id:"family",ar:"مراجعة إعانات الأسرة",nl:"Gezinsregelingen controleren",url:"./articles/childcare-allowance-kinderopvangtoeslag.html",source:"https://www.svb.nl/"},
 {id:"residence",ar:"مراجعة شروط الإقامة",nl:"Verblijfsvoorwaarden controleren",url:"./articles/eu-permanent-residence-netherlands.html",source:"https://ind.nl/"}
];
const copy={ar:{title:"ما الخطوة التالية؟",intro:"اختر المهمة التالية بحسب ما أنجزته في قائمة المهام. تحقق من شروط كل جهة لحالتك.",next:"الخطوة المقترحة",guide:"افتح الدليل",official:"تحقق من المصدر الرسمي",progress:"مهام مكتملة",complete:"أكملت القائمة. راجع المصادر الرسمية عند تغيّر ظروفك.",local:"يُحفظ التقدم على هذا الجهاز فقط.",manage:"افتح قائمة المهام",cv:"أنشئ سيرة ذاتية للعمل"},nl:{title:"Wat is mijn volgende stap?",intro:"Bekijk je volgende taak op basis van je bestaande checklist. Controleer de voorwaarden voor jouw situatie.",next:"Voorgestelde stap",guide:"Open de gids",official:"Controleer de officiële bron",progress:"Taken voltooid",complete:"Je checklist is afgerond. Controleer officiële bronnen als je situatie verandert.",local:"Je voortgang blijft alleen op dit apparaat.",manage:"Open mijn checklist",cv:"Maak een cv voor werk"}};
function lang(){return localStorage.getItem("mbo_site_lang")==="nl"?"nl":"ar"}
function read(){const data=window.MboData.readChecklistState();return data.checks&&typeof data.checks==="object"?data.checks:{}}
function render(){const root=document.getElementById("phase3");if(!root)return;const l=lang(),t=copy[l],checks=read(),done=tasks.filter(x=>checks[x.id]).length,next=tasks.find(x=>!checks[x.id]);root.lang=l;root.dir=l==="ar"?"rtl":"ltr";root.innerHTML=`<div class="p3-card"><h2>${t.title}</h2><p>${t.intro}</p><div class="p3-progress" role="progressbar" aria-valuenow="${done}" aria-valuemin="0" aria-valuemax="${tasks.length}" aria-label="${t.progress}"><span style="width:${done/tasks.length*100}%"></span></div><p class="p3-muted">${t.progress}: ${done} / ${tasks.length} · ${t.local}</p>${next?`<div class="p3-item"><strong>${t.next}: ${next[l]}</strong><div class="p3-tools"><a class="p3-btn primary" href="${next.url}">${t.guide}</a><a class="p3-btn" href="${next.source}" target="_blank" rel="noopener noreferrer">${t.official} ↗</a></div></div>`:`<div class="p3-item">${t.complete}</div>`}<div class="p3-tools"><button class="p3-btn" type="button" id="p3-manage">${t.manage}</button><a class="p3-btn" href="./cv.html">${t.cv}</a></div></div>`;root.querySelector("#p3-manage").addEventListener("click",()=>{const trigger=document.querySelector('[data-p1="check"]');trigger?.click()})}
function mount(){if(document.getElementById("phase3"))return;const main=document.querySelector("main#mainContent");if(!main)return;const root=document.createElement("section");root.id="phase3";root.className="p3";main.prepend(root);render()}
function init(){mount();window.addEventListener("mbo:pagechange",mount);new MutationObserver(render).observe(document.documentElement,{attributes:true,attributeFilter:["lang"]});window.addEventListener("storage",e=>{if(e.key==="mbo_phase1_v1"||e.key==="mbo_site_lang")render()});window.addEventListener("mbo:datachange",render);document.addEventListener("change",e=>{if(e.target.closest("#p1-panel"))queueMicrotask(render)});document.addEventListener("click",e=>{if(e.target.closest("#p1-reset"))queueMicrotask(render)})}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();

/* Phase 3 — Professional AI assistant
 * The official Gabster loader is isolated from the site's own UI and loaded once.
 */
(()=>{"use strict";
const GABSTER_SRC="https://widget.gabster.ai/loader?cbid=6ab64b269dd3b700e6acc092";
function loadGabster(){
  if(document.querySelector('script[data-gabster-widget]')) return;
  const script=document.createElement("script");
  script.src=GABSTER_SRC;
  script.async=true;
  script.defer=true;
  script.setAttribute("data-gabster-widget","");
  script.setAttribute("data-embed-type","widget");
  script.addEventListener("error",()=>{script.remove()},{once:true});
  document.body.appendChild(script);
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",loadGabster,{once:true});
else loadGabster();
})();