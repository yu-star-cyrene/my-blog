import type { SiteConfig } from "@/types/config";
import { fontConfig } from "./fontConfig";

// 定义站点语言
const SITE_LANG = "zh_CN";

export const siteConfig: SiteConfig = {
    // 站点标题
    title: "小余",

    // 站点副标题
    subtitle: "ciallo！！！",

    // 站点 URL
    site_url: "https://sliver-yu.cc",

    // 站点描述
    description: "Firefly 是一款基于 Astro 框架和 Fuwari 模板开发的个人博客主题。",

    // 站点关键词
    keywords: ["Firefly", "Blog", "Astro", "技术博客"],

    // 主题色
    themeColor: {
        hue: 165,
        fixed: false,
        defaultMode: "system",
    },

    // Favicon 配置
    favicon: [
        {
            src: "/assets/images/favicon.ico",
        },
    ],

    // 导航栏配置
    navbar: {
        // 导航栏 Logo
        logo: {
			type: "text",
			value: "",
			alt: "",
		},
        // 导航栏标题
        title: "在下余林阳",
        widthFull: false,
        followTheme: false,
    },

    // 站点开始日期
    siteStartDate: "2026-01-06",

    // 文章更新时间显示
    showLastModified: true,
    outdatedThreshold: 30,

    // 功能开关
    sharePoster: true,
    generateOgImages: false,

    // Bangumi 配置
    bangumi: {
        userId: "1163581",
    },

    // 页面开关
    pages: {
        sponsor: false,
        guestbook: true,
        bangumi: false,
    },

    // 列表布局
    postListLayout: {
        defaultMode: "list",
        allowSwitch: true,
        grid: {
            masonry: false,
            columns: 3,
        },
    },

    // 分页
    pagination: {
        postsPerPage: 10,
    },

    // 统计
    analytics: {
        googleAnalyticsId: "",
        microsoftClarityId: "",
    },

    // 字体与语言
    font: fontConfig,
    lang: SITE_LANG,
};
