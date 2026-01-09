import type { CommentConfig } from "../types/config";

export const commentConfig: CommentConfig = {
    // 强制激活 Twikoo
    type: "twikoo",

    twikoo: {
        envId: "https://twikoo-vercel-ten-beta.vercel.app",
        lang: "zh-CN",
        visitorCount: true,
    },

    // 其他保留默认，防止报错
    waline: { serverURL: "https://waline.vercel.app", lang: "zh-CN", login: "enable", visitorCount: true },
    artalk: { server: "https://artalk.example.com/", locale: "zh-CN", visitorCount: true },
    giscus: { repo: "CuteLeaf/Firefly", repoId: "R_kgD2gfdFGd", category: "General", categoryId: "DIC_kwDOKy9HOc4CegmW", mapping: "title", strict: "0", reactionsEnabled: "1", emitMetadata: "1", inputPosition: "top", lang: "zh-CN", loading: "lazy" },
    disqus: { shortname: "firefly" },
};