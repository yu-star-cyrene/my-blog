import type { AdConfig } from "../types/config";

// 顶部横幅保持不变
export const adConfig1: AdConfig = {
    image: {
        src: "/assets/images/d1.webp",
        alt: "广告横幅",
        link: "#",
        external: true,
    },
    closable: true,
    displayCount: -1,
    padding: { all: "0" },
};

// === 侧边栏点赞卡片 (红色版) ===
export const adConfig2: AdConfig = {
    title: "支持博主", // 标题修改
    
    // 如果你有图片，请确保路径正确；如果没有，可以留空 src
    image: {
        src: "/assets/images/d2.webp", 
        alt: "点赞",
        link: "",
        external: false,
    },

    content: `
    <div style="text-align: center;">
      <p style="font-size: 0.9rem; margin-bottom: 1rem; opacity: 0.8;">
        觉得文章写得不错？<br>点个赞支持一下吧！
      </p>
      
      <button id="global-like-btn" style="
        background: #ef4444; 
        color: white; 
        border-radius: 99px; 
        padding: 8px 24px; 
        font-weight: bold; 
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s;
        border: none;
        outline: none;
        box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.3);
      " onmouseover="this.style.transform='scale(1.05)';this.style.background='#dc2626'" onmouseout="this.style.transform='scale(1)';this.style.background='#ef4444'">
        <span>❤️ 点赞本站</span>
        <span id="global-like-count" style="background:rgba(255,255,255,0.2); padding: 0 8px; border-radius: 12px; font-size: 0.9em;">0</span>
      </button>

      <script>
        (function() {
           const APP_ID = "egB5SxnIsG2BkAqm2c0f15I9-MdYXbMMI";
           const APP_KEY = "Z39KNTONWBkZITawt54qf5eA";
           const SERVER_URL = "https://egb5sxni.api.lncldglobal.com";
           
           function startGlobalLike() {
             if(typeof AV === 'undefined') return;
             if(!AV.applicationId) AV.init({ appId: APP_ID, appKey: APP_KEY, serverURLs: SERVER_URL });
             
             const query = new AV.Query('GlobalLikes');
             const btn = document.getElementById('global-like-btn');
             const count = document.getElementById('global-like-count');
             
             // 获取数据
             query.equalTo('id', 'site_global');
             query.first().then(res => {
               if(res) count.innerText = res.get('likes');
               else count.innerText = '0';
             }).catch(e => { count.innerText = '0'; });

             // 点击事件
             btn.onclick = function() {
               if(btn.dataset.loading) return;
               btn.dataset.loading = "true";
               
               query.first().then(res => {
                 if(res) {
                   res.increment('likes', 1);
                   return res.save();
                 } else {
                   const NewObj = AV.Object.extend('GlobalLikes');
                   const obj = new NewObj();
                   obj.set('id', 'site_global');
                   obj.set('likes', 1);
                   return obj.save();
                 }
               }).then(saved => {
                 count.innerText = saved.get('likes');
                 const originalHTML = btn.innerHTML;
                 btn.innerHTML = "<span>🌹 谢谢!</span>";
                 setTimeout(() => {
                    btn.innerHTML = originalHTML;
                    document.getElementById('global-like-count').innerText = saved.get('likes');
                    delete btn.dataset.loading;
                 }, 1500);
               });
             }
           }

           const timer = setInterval(() => {
             if(window.AV) { startGlobalLike(); clearInterval(timer); }
           }, 500);
        })();
      </script>
    </div>
    `,
    closable: true,
    displayCount: -1,
    padding: { all: "1rem" },
};
