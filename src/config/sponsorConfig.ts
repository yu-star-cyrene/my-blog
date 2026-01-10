import type { SponsorConfig } from "../types/config";

export const sponsorConfig: SponsorConfig = {
    // 页面标题
    title: "点赞夸夸",
    // 页面描述文本
    description: "Give me a like",
    // 赞助用途说明
    usage: "您的每一个赞都是我更新的动力！",
    // 关闭赞助者列表
    showSponsorsList: false,
    // 开启按钮显示（实际显示为点赞按钮）
    showButtonInPost: true,
    // 清空具体支付方式，只留一个占位防止报错
    methods: [
        {
            name: "点赞",
            icon: "material-symbols:thumb-up",
            qrCode: "", 
            link: "",
            description: "点击下方按钮为我点赞",
            enabled: true,
        },
    ],
    sponsors: [],
};
