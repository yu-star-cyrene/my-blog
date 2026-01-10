import type { AdConfig } from "../types/config";

export const adConfig1: AdConfig = {
    image: {
        src: "/assets/images/d1.webp",
        alt: "广告横幅",
        link: "#",
        external: true,
    },
    closable: true,
    displayCount: -1,
    padding: {
        all: "0",
    },
};

export const adConfig2: AdConfig = {
    title: "",
    image: {
        src: "/assets/images/praise.png",
        alt: "求夸夸",
        link: "",
        external: false,
    },
    content: `
    <div style="text-align: center;">
      <p style="font-size: 0.9rem; margin-bottom: 1rem; opacity: 0.8;">
        如果不介意的话，<br>可以给小余一点鼓励吗？(✿◡‿◡)
      </p>
      
      <button id="global-like-btn" style="
        background: var(--primary); 
        color: white; 
        border-radius: 99px; 
        padding: 8px 20px; 
        font-weight: bold; 
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s;
        border: none;
        outline: none;
      " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
        <span>👍 夸夸我</span>
        <span id="global-like-count" style="background:rgba(255,255,255,0.2); padding: 0 6px; border-radius: 10px; font-size: 0.8em;">0</span>
      </button>

      <script>
        (function() {
           const APP_ID = "egB5SxnIsG2BkAqm2c0f15I9-MdYXbMMI";
           const APP_KEY = "Z39KNTONWBkZITawt54qf5eA";
           const SERVER_URL = "https://egb5sxni.api.lncldglobal.com";
           
           function initAndRun() {
             if(!AV.applicationId) AV.init({ appId: APP_ID, appKey: APP_KEY, serverURLs: SERVER_URL });
             
             const query = new AV.Query('GlobalLikes');
             const btn = document.getElementById('global-like-btn');
             const count = document.getElementById('global-like-count');
             
             // 获取数据
             query.equalTo('id', 'site_global');
             query.first().then(res => {
               if(res) count.innerText = res.get('likes');
             }).catch(e => console.log('暂无数据，显示默认0'));

             // 点击
             btn.onclick = function() {
               if(btn.dataset.loading) return;
               btn.dataset.loading = "true";
               
               query.first().then(res => {
                 if(res) { res.increment('likes', 1); return res.save(); }
                 else {
                   const NewObj = AV.Object.extend('GlobalLikes');
                   const obj = new NewObj();
                   obj.set('id', 'site_global');
                   obj.set('likes', 1);
                   return obj.save();
                 }
               }).then(saved => {
                 count.innerText = saved.get('likes');
                 const old = btn.innerHTML;
                 btn.innerHTML = "<span>❤️ 收到!</span>";
                 setTimeout(() => { 
                    btn.innerHTML = old; 
                    document.getElementById('global-like-count').innerText = saved.get('likes');
                    delete btn.dataset.loading; 
                 }, 1500);
               }).catch(e => { delete btn.dataset.loading; });
             }
           }

           if (typeof AV === 'undefined') {
               const script = document.createElement('script');
               script.src = 'https://cdn.jsdelivr.net/npm/leancloud-storage@4.15.0/dist/av-min.js';
               script.onload = initAndRun;
               document.head.appendChild(script);
           } else { initAndRun(); }
        })();
      </script>
    </div>
    `,
    closable: true,
    displayCount: -1,
    padding: { all: "1rem" },
};
