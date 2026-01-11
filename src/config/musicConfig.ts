import type { MusicPlayerConfig } from "../types/config";

export const musicPlayerConfig: MusicPlayerConfig = {
    enable: true,
    mode: "local",
    meting: {
        api: "https://api.injahow.cn/meting/?server=:server&type=:type&id=:id",
        server: "kugou",
        type: "playlist",
        id: "1954502", 
        auth: "",
        fallbackApis: [
            "https://api.injahow.cn/meting/?server=:server&type=:type&id=:id",
            "https://api.moeyao.cn/meting/?server=:server&type=:type&id=:id",
        ],
        jsPath: "https://unpkg.com/meting@2/dist/Meting.min.js",
    },
    local: {
        playlist: [
            {
                name: "成仙",
                artist: "王朝1982",
                url: "/assets/music/阿哲的音乐信箱 - 王朝1982 (成仙).mp3",
                cover: "/assets/music/cover/成仙.jpg",
                lrc: "/assets/music/lrc/王朝1982.lrc"
            },
            {
                name: "坐忘道",
                artist: "王朝1982",
                url: "/assets/music/李同学yy - 王朝1982 (坐忘道).mp3",
                cover: "/assets/music/cover/坐忘道.jpg",
                lrc: "/assets/music/lrc/在银河中孤独摇摆.lrc"
            }, // <-- 已补齐逗号
            {
                name: "登阶",
                artist: "b站up主道雀Bzz",
                url: "/assets/music/登阶.mp3",
                cover: "/assets/music/cover/登阶.jpg",
                lrc: "/assets/music/lrc/在银河中孤独摇摆.lrc"
            }, // <-- 已补齐逗号
			{
                name: "在银河中孤独摇摆",
                artist: "知更鸟",
                url: "/assets/music/知更鸟、HOYO-MiX、Chevy - 在银河中孤独摇摆 (Sway to My Beat in Cosmos).flac",
                cover: "/assets/music/cover/知更鸟.jpg",
                lrc: "/assets/music/lrc/王朝1982.lrc"
            }, // <-- 已补齐逗号
            {
                name: "使一颗心免于哀伤",
                artist: "知更鸟",
                url: "/assets/music/知更鸟、HOYO-MiX、Chevy - 使一颗心免于哀伤 (If I Can Stop One Heart From Breaking).flac",
                cover: "/assets/music/cover/知更鸟.jpg",
                lrc: "/assets/music/lrc/在银河中孤独摇摆.lrc"
            }, // <-- 已补齐逗号
            {
                name: "希望有羽毛和翅膀",
                artist: "知更鸟",
                url: "/assets/music/知更鸟、HOYO-MiX、Chevy - 希望有羽毛和翅膀 (Hope Is the Thing With Feathers).flac",
                cover: "/assets/music/cover/知更鸟.jpg",
                lrc: "/assets/music/lrc/在银河中孤独摇摆.lrc"
            }, // <-- 已补齐逗号
            {
                name: "若我不曾见过太阳",
                artist: "知更鸟",
                url: "/assets/music/知更鸟、HOYO-MiX、Chevy - 若我不曾见过太阳 (Had I Not Seen the Sun).flac",
                cover: "/assets/music/cover/知更鸟.jpg",
                lrc: "/assets/music/lrc/在银河中孤独摇摆.lrc"
            }
        ],
    },
    player: {
        autoplay: false,
        theme: "var(--btn-regular-bg)",
        loop: "all",
        order: "list",
        preload: "auto",
        volume: 0.7,
        mutex: true,
        lrcType: 3,
        lrcHidden: true,
        listFolded: false,
        listMaxHeight: "340px",
        storageName: "aplayer-setting",
    },
    responsive: {
        mobile: {
            hide: false,
            breakpoint: 768,
        },
    },
};