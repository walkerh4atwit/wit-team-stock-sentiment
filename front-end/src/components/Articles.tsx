import { ReactElement, useEffect, useState } from "react";
import '../styles/my-Articles.css'
import '../styles/my-Card.css'
import '../styles/my-Gradient.css'

interface IArticleList {
    category: string,
    list: any[]
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
                await fetch("https://" + backEndHost + "/articles/" + props.type + "/" + props.id + "/" + score)
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
        
        return articleList.list.map(
            (article: string[]) => {
                return (<div key={article[1]} className="my-Card">
                    <div className="my-Card-Header my-Header-Gradient">{article[0]}</div>
                    <a href={article[1]} className="my-Article-Card-Body">Go to article!</a>
                </div>)
            }
        )
    }

    return (
        <div className="my-Articles">
            <div className="my-Article-Column">
                <div className="my-Article-Title">Positive</div>
                {mapArticles(positive)}
            </div>
            <div className="my-Article-Column">
                <div className="my-Article-Title">Neutral</div>
                {mapArticles(neutral)}
            </div>
            <div className="my-Article-Column">
                <div className="my-Article-Title">Negative</div>
                {mapArticles(negative)}
            </div>
        </div>
    )
}

export default Articles;