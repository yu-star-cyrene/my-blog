import {
    LinkPreset,
    type NavBarConfig,
    type NavBarLink,
    type NavBarSearchConfig,
    NavBarSearchMethod,
} from "../types/config";
import { siteConfig } from "./siteConfig";

// 根据页面开关动态生成导航栏配置
const getDynamicNavBarConfig = (): NavBarConfig => {
    // 基础导航栏链接：只保留主页和归档
    const links: (NavBarLink | LinkPreset)[] = [
        LinkPreset.Home,
        LinkPreset.Archive,
    ];

    // 如果以后需要添加自定义菜单，可以在这里 links.push(...)

    // 留言板控制：根据 siteConfig 决定是否显示
    if (siteConfig.pages.guestbook) {
        links.push(LinkPreset.Guestbook);
    }

    // 关于页面
    links.push(LinkPreset.About);

    return { links } as NavBarConfig;
};

// 导航搜索配置
export const navBarSearchConfig: NavBarSearchConfig = {
    // 默认使用 PageFind (适合静态博客，无需后端)
    method: NavBarSearchMethod.PageFind,

    // MeiliSearch 配置（如果你没有部署 MeiliSearch 服务，这部分保持默认即可，不会生效）
    meiliSearchConfig: {
        INDEX_NAME: "posts",
        CONTENT_DIR: "src/content/posts",
        MEILI_HOST: "http://localhost:7700",
        PUBLIC_MEILI_HOST: "http://localhost:7700",
        PUBLIC_MEILI_SEARCH_KEY:
            "41134b15079da66ca545375edbea848a9b7173dff13be2028318fefa41ae8f2b",
    },
};

export const navBarConfig: NavBarConfig = getDynamicNavBarConfig();