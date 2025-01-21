import { ReactElement, useEffect, useState } from "react";
import '../styles/my-Articles.css'
import '../styles/my-Card.css'

interface IArticle {
    url: string,
    headline: string
}

interface IArticleList {
    category: string,
    list: IArticle[]
}

const Articles = (props: {type: string, id: string}) => {
    const [positive, setPositive] = useState<IArticleList>(
        {
            category: "Positive",
            list: []
        }
    )

    const [neutral, setNeutral] = useState<IArticleList>(
        {
            category: "Neutral",
            list: []
        }
    )

    const [negative, setNegative] = useState<IArticleList>(
        {
            category: "Negative",
            list: []
        }
    )

    // this differentiates the server between dev and prod
    const backEndHost =
        process.env.REACT_APP_API_URL

    const pullData = async (score: number) => {
        try {
            const response = 
                await fetch("https://" + backEndHost + "/articles/" + "ticker" + "/" + props.id + "/" + score)
            const data = await response.json()
            if (score == 2) {
                setPositive({
                    category: "Positive",
                    list: data
                })
            }
            else if (score == 1) {
                setNeutral({
                    category: "Neutral",
                    list: data
                }); 
            }
            else {
                setNegative({
                    category: "Negative",
                    list: data
                }); 
            }   
        }
        catch { }
    }

    useEffect(() => { 
        pullData(2);
        pullData(1);
        pullData(0);
    }, [])

    const mapArticles = (articleList: IArticleList) => {
        // console.log(props.type)
        return articleList.list.map(
            (article: IArticle) => {
                return (<div className="my-Card">
                    <div className="my-Card-Header">{article.headline}</div>
                    <a href={article.url}>Go to article!</a>
                </div>)
            }
        )
    }

    return (
        <div className="my-Articles">
            <div>
                <div className="my-Article-Title">Positive</div>
                {mapArticles(positive)}
            </div>
            <div>
                <div className="my-Article-Title">Neutral</div>
                {mapArticles(neutral)}
            </div>
            <div>
                <div className="my-Article-Title">Negative</div>
                {mapArticles(negative)}
            </div>
        </div>
    )
}

export default Articles;